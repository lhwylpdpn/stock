//+------------------------------------------------------------------+
//|                                                         test.mq4 |
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
//---   
   string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];               // An array to get strings
   //--- Get the separator code


    //- order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);

      
   
          if(TimeMinute(TimeCurrent())==1)
 
                     
            if(TimeMinute(TimeCurrent())!=5)
            {
               string filename="API.txt";
               int filehandle=FileOpen(filename,FILE_READ|FILE_TXT);
                                 while(!FileIsEnding(filehandle))
                                 {
                           
                                    u_sep=StringGetCharacter(sep,0);
                              //--- Split the string to substrings
                                    int k=StringSplit(FileReadString(filehandle),u_sep,result);
                              //--- Show a comment 
                           
                              //--- Now output all obtained strings
                              if(k>0)
                                {
                                 for(int i=0;i<k;i++)
                                   {
                                    PrintFormat("result[%d]=%s",i,result[i]);
                                   order_send(result[0],result[2],float(result[1]),float(result[3]),float(result[4]),float(result[5]));
                                 //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
                                   }
                                }}
                                      FileClose(filehandle);
                                      Print("test");
 
}}





  }
  int order_send (string buy_id,string sell_id,float buyprice,float sellprice,float except_buy_price, float except_sell_price )
  {
//--- 
      int ticket_buy;
      int ticket_sell;
        ticket_buy=OrderSend(buy_id,OP_BUY,0.01,Ask,3,0,0,"",1,0);
        ticket_sell=OrderSend(sell_id,OP_SELL,0.01,Ask,3,0,0,"",1,0);
        printf("buy"+ticket_buy);
        printf("sell"+ticket_sell);
      int re=order_close(ticket_buy,ticket_sell,buy_id,sell_id,buyprice,sellprice,except_buy_price,except_sell_price);
         if(re=1)
           {
            return(0);
             }
        return(1);
        }

  
//---
  void update_data(int filehandle,string name)
{   
   string str=name+","+string(iTime(name,0,0))+","+string( iOpen(name,0,0))+","+string(iHigh(name,0,0))+","+string(iLow(name,0,0))+","+string(iClose(name,0,0));
   FileWriteString(filehandle,str+"\r\n");
 }
  
  int order_close(int ticket_buy,int ticket_sell,string buy_id,string sell_id,float buyprice,float sellprice,float except_buy_price, float except_sell_price)
  {
   int p1=1;
   int p2=1;
      while(p1==1 || p2==1 )
        {
        
  
         p1=OrderClose(ticket_buy,0.01,except_buy_price,3,Red);
         p2=OrderClose(ticket_sell,0.01,except_sell_price,3,Red);

          }
  
  
  return(1);
  }
//+------------------------------------------------------------------+
void get_data()
{ string filename2="API_callback.csv";
                 int filehandle2=FileOpen(filename2,FILE_WRITE|FILE_CSV);  
                 
                printf(TimeMinute(TimeCurrent()));
                update_data(filehandle2,"USDCHF");
                update_data(filehandle2,"GBPCHF");
                update_data(filehandle2,"EURCHF");
                FileClose(filehandle2);}
void order_open()
{
              string filename="API.txt";
               int filehandle=FileOpen(filename,FILE_READ|FILE_TXT);
                                 while(!FileIsEnding(filehandle))
                                 {
                           
                                    u_sep=StringGetCharacter(sep,0);
                              //--- Split the string to substrings
                                    int k=StringSplit(FileReadString(filehandle),u_sep,result);
                              //--- Show a comment 
                           
                              //--- Now output all obtained strings
                              if(k>0)
                                {
                                 for(int i=0;i<k;i++)
                                   {
                                    PrintFormat("result[%d]=%s",i,result[i]);
                                   order_send(result[0],result[2],float(result[1]),float(result[3]),float(result[4]),float(result[5]));
                                 //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
                                   }
                                }}
                                      FileClose(filehandle);}