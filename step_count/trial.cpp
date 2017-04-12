int Threshold = 100;
int Hit;
void setup(){

  pinMode (13,OUTPUT);
  BlinkLed (3,500);
  Serial.begin(38400);

}

void loop(){
  for (int i = 0;i<=5;i++){                //  Cycle through ADC channels.
    if (analogRead(i)>Threshold){          //  If current channel reading exceeds threshold
      Hit = AnalogMaxima(i,Threshold,2);  //  find local maxima and return value.
      if (Hit == 1025 || Hit == 0){        //  if still ascending or below threshold,
        break;                             //  go to next ADC channel.
      }
      else{
        Serial.println(Hit);               //  Show maxima. or play midi note ;)
      }
    }
  }
}


//--------------------------------------------------------------------------------
/* AnalogMaxima compares succesive readings from ADC on channel AnalogCh
and returns :
   1025 if voltage is decreasing,so that only the maxima is returned.
   0    if below threshold.
   or returns the highest value when voltage starts to drop (local maxima).

AnalogCh  :  Channel on the ADC to check for maxima.
Threshold :  Lowest voltage reading to begin maxima evaluation.
Delay     :  Delay between succesive readings.
*/

int AnalogMaxima (int AnalogCh, int Threshold, int Delay){    
  int check1;                                  //variable to store first reading.
  int check2;                                  //variable to store second reading.

  check1 = analogRead(AnalogCh);               //Assing first reading 
  delay(Delay);                                //wait
  check2 = analogRead (AnalogCh);              //Assing second reading.
  if (check1>check2){                          //If voltage is DECREASING (no maxima)...
    return 1025;                               //end loop and return 1025.
  }
  else{
    while (analogRead(AnalogCh)>Threshold){     //While above threshold and RISING
      check1 = analogRead(AnalogCh);            //Assing first reading
      delay(Delay/2);                           //wait
      check2 = analogRead (AnalogCh);           //Assing second reading.
      delay(Delay/2);                           //wait,and loop unless...
      if (check1>check2){                       //voltage drop is observed
        return check1;                          //if so return highest value :)

      }
    }
  }
}                            // end of AnalogMaxima //
//--------------------------------------------------------------------------------


//--------------------------------------------------------------------------------
/* BlinkLed ensures there is enough time in the start of the sketch to download a
new sketch if desired,in case that the serial tx is constantly sending data.
Times  :  times to blink.
Delay  :  delay between blinks.
*/

void BlinkLed (int Times, int Delay){
  for (int i = 1; i<=Times; i++){
    digitalWrite (13,HIGH);
    delay(Delay);
    digitalWrite (13,LOW);
    delay(Delay);
  }
}                             // end of BlinkLed //
//--------------------------------------------------------------------------------
