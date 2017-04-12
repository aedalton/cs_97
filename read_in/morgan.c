#include <compat/deprecated.h>
#include <FlexiTimer2.h>
#define SAMPFREQ 256                      // ADC sampling rate 256
#define TIMER2VAL (1024/(SAMPFREQ))       // Set 256Hz sampling frequency                    
volatile unsigned char CurrentCh=0;         //Current channel being sampled.
volatile unsigned int ADC_Value = 0;
 //ADC current value

void setup() {

 noInterrupts();  // Disable all interrupts before initialization
 
 FlexiTimer2::set(TIMER2VAL, Timer2_Overflow_ISR);
 FlexiTimer2::start();
 
 // Serial Port
 Serial.begin(57600);

 interrupts();  // Enable all interrupts after initialization has been completed
}

void Timer2_Overflow_ISR()
{
        ADC_Value = analogRead(CurrentCh);
        //Serial.print("D!");    //this is packet header for my application
        Serial.println(ADC_Value);
}

void loop() {
 __asm__ __volatile__ ("sleep");
}
