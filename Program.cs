using System;
using System.Diagnostics;

namespace vmpoStudy03
{
    class Program
    {
        static void Main(string[] args)
        {
            //프로세스 파일명 정의
            //파이썬 exe를 직접 실행해서 파이썬 코드가 실행되도록 한다.
            var psi = new ProcessStartInfo();
            psi.FileName = @"C:\python38-64\python.exe"; //파이썬 설치 경로
            //                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              psi.Arguments = $"\"C:\\dev532\\python\\py532\\s01\\test.py\""; //파일경로                                                  
            psi.Arguments = $"\"C:\\Users\\tim96\\Downloads\\python_unity.py\"";
            //3) Proecss configuration  
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;

            //4) return value def
            var erros = "";
            var results = "";

            using (var process = Process.Start(psi))
            {
                erros = process.StandardError.ReadToEnd();
                results = process.StandardOutput.ReadToEnd();
            }

            Console.WriteLine(erros);
            Console.WriteLine(results);

        }
    }
}
