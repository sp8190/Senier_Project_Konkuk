using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net.Sockets;
using System.Text;
using System.Net;

public class _TextureReceiver : MonoBehaviour
{
    public int port = 5000;
    public string IP = "127.0.0.1";
    TcpClient client;

    [HideInInspector]
    public Texture2D texture;

    private bool stop = false;

    [Header("Must be the same in sender and receiver")]
    public int messageByteLength = 24;

    // Use this for initialization
    void Start()
    {
        Application.runInBackground = true;

        client = new TcpClient();

        //Connect to server from another Thread
        Loom.RunAsync(() => {
            // if on desktop
            // client.Connect(IPAddress.Loopback, port);
            client.Connect(IPAddress.Parse(IP), port);

            imageReceiver();
        });
    }
    void imageReceiver()
    {
        //While loop in another Thread is fine so we don't block main Unity Thread
        Loom.RunAsync(() => {
            while (!stop)
            {
                //Read Image Count
                int imageSize = readImageByteSize(messageByteLength);

                //Read Image Bytes and Display it
                readFrameByteArray(imageSize);
                //readFrameByteArray(12288000);
            }
        });
    }

    //Converts the byte array to the data size and returns the result
    int frameByteArrayToByteLength(byte[] frameBytesLength)
    {
        /*if (BitConverter.IsLittleEndian)
         {
             Array.Reverse(frameBytesLength);
             UnityEngine.Debug.Log("- BitConverter.IsLittleEndian");
         }*/
        var sb = new StringBuilder("frameBytesLength[] { ");
        foreach (var b in frameBytesLength)
        {
            sb.Append(b + ", ");
        }
        sb.Append("}");
        UnityEngine.Debug.Log(sb.ToString());
        //int byteLength = BitConverter.ToInt32(frameBytesLength, 0);
        int byteLength = frameBytesLength[0] + frameBytesLength[1] * 256;
        return byteLength;
    }

    private int readImageByteSize(int size)
    {
        UnityEngine.Debug.Log("- image byte size: " + size);
        bool disconnected = false;

        NetworkStream serverStream = client.GetStream();
        UnityEngine.Debug.Log("- serverStream: " + serverStream);
        byte[] imageBytesCount = new byte[size];
        var total = 0;
        do
        {
            var read = serverStream.Read(imageBytesCount, total, size - total);
            UnityEngine.Debug.LogFormat("Client recieved " + read + " bytes");
            if (read == 0)
            {
                disconnected = true;
                break;
            }
            total += read;
            UnityEngine.Debug.Log("- image byte read: " + read);
            UnityEngine.Debug.Log("- image byte total: " + total);
        } while (total != size);
        UnityEngine.Debug.Log("- break While");
        int byteLength;

        if (disconnected)
        {
            UnityEngine.Debug.Log("disconnected");
            byteLength = -1;
        }
        else
        {
            byteLength = frameByteArrayToByteLength(imageBytesCount);
        }

        return byteLength;
    }

    private void readFrameByteArray(int size)
    {
        bool disconnected = false;
        UnityEngine.Debug.Log("- image size: " + size);
        NetworkStream serverStream = client.GetStream();
        byte[] imageBytes = new byte[size];
        var total = 0;
        //do{
        var read = serverStream.Read(imageBytes, total, size - total);
        if (read == 0)
        {
            disconnected = true;
            //break;
        }
        total += read;
        UnityEngine.Debug.Log("- read: " + read);
        UnityEngine.Debug.Log("- total: " + total);
        //} while (total != size);
        byte[] imageBytes2 = new byte[read];
        imageBytes.CopyTo(imageBytes2, 0);

        UnityEngine.Debug.Log("break while");

        var sb = new StringBuilder("imageBytes[] { ");
        foreach (var b in imageBytes2)
        {
            sb.Append(b + ", ");
        }
        sb.Append("}");
        UnityEngine.Debug.Log(sb.ToString());

        bool readyToReadAgain = false;

        //Display Image
        if (!disconnected)
        {
            //Display Image on the main Thread
            Loom.QueueOnMainThread(() => {
                loadReceivedImage(imageBytes2);
                readyToReadAgain = true;
            });
        }

        //Wait until old Image is displayed
        while (!readyToReadAgain)
        {
            System.Threading.Thread.Sleep(1);
        }
    }


    void loadReceivedImage(byte[] receivedImageBytes)
    {
        if (texture) texture.LoadImage(receivedImageBytes);
    }

    public void SetTargetTexture(Texture2D t)
    {
        texture = t;
    }

    void OnApplicationQuit()
    {
        stop = true;

        if (client != null)
        {
            client.Close();
        }
    }
}