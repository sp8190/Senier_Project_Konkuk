#include <stdio.h>
#include <wiringPi.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>

#define MOTOR1A 1 // BCM_GPIO 26
#define MOTOR1B 2 // BCM_GPIO 19
#define MOTOR2A 3 // BCM_GPIO 13
#define MOTOR2B 4 // BCM_GPIO 6

int getch(void)
{
    struct termios oldt,
    newt;
    int ch;

    tcgetattr( STDIN_FILENO, &oldt );
    newt = oldt;

    newt.c_lflag &= ~( ICANON | ECHO );
    tcsetattr( STDIN_FILENO, TCSANOW, &newt );

    ch = getchar();
    tcsetattr( STDIN_FILENO, TCSANOW, &oldt );

    return ch;
}

int kbhit(void)
{
  struct termios oldt, newt;
  int ch;
  int oldf;

  tcgetattr(STDIN_FILENO, &oldt);
  newt = oldt;
  newt.c_lflag &= ~(ICANON | ECHO);

  tcsetattr(STDIN_FILENO, TCSANOW, &newt);
  oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
  fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);

  ch = getchar();
 
  tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
  fcntl(STDIN_FILENO, F_SETFL, oldf);
 
  if(ch != EOF)
  {
    ungetc(ch, stdin);
    return 1;
  }
 
  return 0;
}



void forward() {
    digitalWrite (MOTOR1A, 1) ;
    digitalWrite (MOTOR1B, 0) ;
    digitalWrite (MOTOR2A, 1) ;
    digitalWrite (MOTOR2B, 0) ;
}

void back() {
    digitalWrite (MOTOR1A, 0) ;
    digitalWrite (MOTOR1B, 1) ;
    digitalWrite (MOTOR2A, 0) ;
    digitalWrite (MOTOR2B, 1) ;
}

void leftTurn() {
    digitalWrite (MOTOR1A, 0) ;
    digitalWrite (MOTOR1B, 1) ;
    digitalWrite (MOTOR2A, 1) ;
    digitalWrite (MOTOR2B, 0) ; 
}

void rightTurn() {
    digitalWrite (MOTOR1A, 1) ;
    digitalWrite (MOTOR1B, 0) ; 
    digitalWrite (MOTOR2A, 0) ; 
    digitalWrite (MOTOR2B, 1) ; 
}

void stop() {
    digitalWrite (MOTOR1A, 0) ;
    digitalWrite (MOTOR1B, 0) ; 
    digitalWrite (MOTOR2A, 0) ;
    digitalWrite (MOTOR2B, 0) ; 
}

int main (void)
{
  if (wiringPiSetup() == -1) {
    return 1 ;
  }

  int key;
  pinMode (MOTOR1A, OUTPUT) ;
  pinMode (MOTOR1B, OUTPUT) ;
  pinMode (MOTOR2A, OUTPUT) ;
  pinMode (MOTOR2B, OUTPUT) ;
  stop();

  while(1) {
    if(kbhit()) {
      key=getch();
      switch(key) {
        case 'w':
          forward();
          break;

        case 's':
          stop();
          break;

        case 'a':
          leftTurn();
          break;

        case 'd':
          rightTurn();
          break;

        case 'x':
          back();
          break;

        case 'p':
          stop();
          return 0;
      }
    }
  }  
  return 0 ;
}
