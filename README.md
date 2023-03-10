# OptionChain from AngelOne

    This information is correct on 18.02.2023, SmartAPI MAY change their API.


## How to?


**Settings**

For proper working of the programm, firstly you should create settings.txt file in root of programm.
Fill it with format of example below:

> API_KEY:####;ID:####;PASSWORD:####;OTP_CODE:####

You may change the way of programm getting settings by changing `InitSettings` class in settings.py module.

**Using**

After making settings.txt file you`ll start main.py and every 3 minutes you will have updated .txt files of OPTIDX data in root of your programm. Each file have time of last update in first row, and contains all data provided about option.

**Example of output data:**

> 19:45:32 <br />
> key:value/key:value/key:value/.../key:value <br />
> key:value/key:value/.../key:value/key:value <br />
> key:value/.../key:value/key:value/key:value <br />

## Change the output format or way

**Change the format of data**

To change the format of saved data you have to go into output_processor.py and change method 
parse_options_data_into_string. It gets python dictionary with format below:

    {
       "CE":{
       }"PE":{
       }
    }

CE is Call data; PE is Put data.
Each have the dictionary of properties from Instrument list and WebSocket2.0 merged.

Instrument List - https://smartapi.angelbroking.com/docs/Instruments

WebSocket2.0 - https://smartapi.angelbroking.com/docs/WebSocket2

All the properties you can check in the SmartApi documentation in part about WebSocket2.0 (Snap Quote).

**Change the way programm saving data**

To change the way programm saving option data you have to go into output_processor.py and change method `_push` in it. This method is working with `options_store_key_name` dictionary where you have this structure:

    {
       "BANKNIFTY":{
          "SYMBOL1":{
             "CE":{},
             "PE":{}
          }
          "SYMBOL2":{
             "CE":{},
             "PE":{}
          }
       }
       "NIFTY":{
          "SYMBOL1":{
             "CE":{},
             "PE":{}"
          }
          "SYMBOL2":{
             "CE":{},
             "PE":{}"
          }
       }
       ...
    }
