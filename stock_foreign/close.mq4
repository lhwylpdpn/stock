//+------------------------------------------------------------------+
//|                                                        close.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {

  for(int i=15273000;i<15274509;i++)
  {OrderClose(i,0.01,Ask,0.01,Red);
   printf(GetLastError());}


}
//+------------------------------------------------------------------+
void update_data(int filehandle,string name)
{   
   string str=name+","+string(iTime(name,0,0))+","+string( iOpen(name,0,0))+","+string(iHigh(name,0,0))+","+string(iLow(name,0,0))+","+string(iClose(name,0,0));
   FileWriteString(filehandle,str+"\r\n");
 }