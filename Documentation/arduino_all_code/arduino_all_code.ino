/*************************************************/
/*      ACM Soda Machine Dispensery Systems      */
/*      Written by - Nic Pereira                 */
/*      Circuitry by - Nathan Szanto             */
/*      Arduino uses a C based language,         */
/*       other documentation can be found here:  */
/*       http://arduino.cc/en/Reference/HomePage */
/*************************************************/

//NOTES OF CODE:
//1. Current code does not support sodas having different prices.

//motor switches for dispense duration
//buttons for dispense
//motor switches for lights
//card swipe for money

const int Button[8] = {A8, A9, A10, A11, A12, A13, A14, A15};
const int Motor[8] =  {44, 43, 42, 45, 46, 47, 48, 49};
const int MotorSw[8] = {41, 40, 39, 38, 37, 36, 35, 34};
const int StockSw[8] = {A0, A1, A2, A3, A4, A5, A6, A7};
const int TIME = 2*(1000);

void serialFlush()
{
  while(Serial.available())
  {
    int clearBuffer = Serial.read();
    delay(1);
  }
  Serial.flush();
}

void setup()
{
  /////
  // Settings up the defaults for the Pi.
  // Buttons, Stock Switches, and Motor Switches must be set to INPUT_PULLUP
  // for proper interaction, see look online for INPUT_PULLUP documentation
  // for more information..
  /////
  Serial.begin(9600);
  serialFlush();
  for(int i = 0; i< 8; i++)
  {
    pinMode(Button[i], INPUT_PULLUP);
    pinMode(StockSw[i], INPUT_PULLUP);
    pinMode(MotorSw[i], INPUT_PULLUP);
  }
}

void loop()
{
  bool transFinished = false;
  if(Serial.available())
  {
    /////
    // Read the character sent by the Raspberry Pi to the Arduino to see the
    // state of the transacation
    /////
    char valLetter = (char)Serial.read();
    if(valLetter == 'a')
    {
      while(!transFinished)
      {
        /////
        // Cycles through all of the buttons on the panel and checks if any
        // of them are pressed
        /////
        for(int i = 0; i< 8;)
        {
          //////
          // Checks to make sure that the transacation has not timed output
          //////
          if(!Serial.available())
          {
            if(digitalRead(Button[i]) == LOW)
            {
              /////
              // Checks to see if the soda the user selets is still in stock
              /////
              if(digitalRead(StockSw[i]) == HIGH)
              {
                /////
                // Regulating the motor to properly dispense the soda.
                // (I.E. it turns until it fully completes a revolution).
                /////
                digitalWrite(Motor[i], HIGH);
                delay(TIME);
                while(digitalRead(MotorSw[i]) == LOW);
                digitalWrite(Motor[i], LOW);

                /////
                // Write the the Pi that the transaction was successful
                /////
                Serial.write("s");
                /////
                // Write to the Pi which soda that the user ordered and finish
                // transaction.
                /////
                Serial.print(i);
                transFinished = true;
                break;
              }
              else
              {
                //////
                // Writes to the Pi that the soda is out of stock and ends
                // transaction.
                /////
                Serial.write('o');
                transFinished = true;
                break;
              }
            }
            else
            {
              /////
              // Manually progressing the For loop for better control
              /////
              i++;
            }
          }
          else
          {
            /////
            // Checks to see if it reads the Timeout character from the
            // Pi. If so, it ends the transaction
            /////
            if((char)Serial.read() == 't')
            {
              transFinished = true;
              break;
            }
          }
        }
      }
    }
    else
    {
      Serial.write("e"); //Signals that transaction failed
    }
  }
  /////
  // Resets the transaction state.
  /////
  serialFlush();
}
