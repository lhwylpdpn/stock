//+------------------------------------------------------------------+
//|                                                        test2.mq4 |
//|                        Copyright 2015, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2015, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#property strict
//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+

string filename_all;
int filehandle_all;
int OnInit()
  {
//--- create timer
   EventSetTimer(3);
      filename_all="balance.txt";
      filehandle_all=FileOpen(filename_all,FILE_READ|FILE_WRITE|FILE_TXT);
     
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
      FileClose(filehandle_all);
  }
//+------------------------------------------------------------------+
//| Expert tick function                                             |
//+------------------------------------------------------------------+
void OnTick()
  {
//---
  order_close();
  }
//+------------------------------------------------------------------+
//| Timer function                                                   |
//+------------------------------------------------------------------+
void OnTimer()
  {

  
   //+------------------------------------------------------------------+如果时间是01 且文件是空，创建文件 
  if(TimeMinute(TimeCurrent())==1 && is_null_file("API_callback.csv")==0)
    { Print("数据输出成功");
      get_data();
  }

   if(is_null_file("API.txt")!=0)
     {Print("有建仓需求");
      read_API();
     }
     


  }
  
//+------------------------------------------------------------------+
//| Tester function                                                  |
//+------------------------------------------------------------------+
double OnTester()
  {
//---
   double ret=0.0;
//---

//---
   return(ret);
  }


  int is_null_file(string filename)
  { int h=FileOpen(filename,FILE_READ|FILE_TXT);
    int size= FileSize(h);
    FileClose(h);
    return(size);
   }
   //+------------------------------------------------------------------+读取API函数      
  void read_API()
  {string filename="API.txt";
   string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];
   int filehandle=FileOpen(filename,FILE_READ|FILE_WRITE|FILE_TXT);
      while(!FileIsEnding(filehandle))
      {

         u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filehandle),u_sep,result);
   //--- Show a comment 

   //--- Now output all obtained strings
        order_send(result[0],result[2],float(result[1]),float(result[3]),float(result[4]),float(result[5]));
      //-order_send("EURCHF","GBPCHF",1,1,1.0423,1.4315);
        
        
        
        
     }
     
       FileClose(filehandle);
       FileDelete(filename);
   }
   //+------------------------------------------------------------------+建仓函数      
  void order_send (string buy_id,string sell_id,float buyprice,float sellprice,float except_buy_price, float except_sell_price )
  { 
//--- 
      int ticket_buy;
      int ticket_sell;
        ticket_buy=OrderSend(buy_id,OP_BUY,0.01,Ask,3,0,0,"",1,0);
        ticket_sell=OrderSend(sell_id,OP_SELL,0.01,Bid,3,0,0,"",1,0);
     FileWrite(filehandle_all,string(ticket_buy)+","+string(ticket_sell)+","+string(except_buy_price)+","+string(except_sell_price));
     
        }

  
//+------------------------------------------------------------------+ 写入数据函数
  void update_data(int filehandle,string name)
{   
   string str=name+","+string(iTime(name,0,0))+","+string( iOpen(name,0,0))+","+string(iHigh(name,0,0))+","+string(iLow(name,0,0))+","+string(iClose(name,0,0));
   FileWriteString(filehandle,str+"\r\n");
 }
 
//+------------------------------------------------------------------+ 获得外汇价格数据
void get_data()
{ string filename2="API_callback.csv";
                 int filehandle2=FileOpen(filename2,FILE_WRITE|FILE_CSV);  
                 
             
                update_data(filehandle2,"USDCHF");
                update_data(filehandle2,"GBPCHF");
                update_data(filehandle2,"EURCHF");
                update_data(filehandle2,"EURUSD");
                update_data(filehandle2,"USDJPY");
                update_data(filehandle2,"AUDUSD");
                update_data(filehandle2,"GBPUSD");
                update_data(filehandle2,"USDCAD");
                update_data(filehandle2,"EURGBP");
                FileClose(filehandle2);}



//+------------------------------------------------------------------+ 平仓函数                                     
     void order_close()
  {string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];
   string buy_ticket="";
   string sell_ticket="";
   FileSeek(filehandle_all,0,0);

   while(!FileIsEnding(filehandle_all))
   {           
   u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filehandle_all),u_sep,result);
      if(OrderSelect(result[0], SELECT_BY_TICKET,MODE_TRADES) && OrderCloseTime()==0 && OrderSelect(result[1], SELECT_BY_TICKET,MODE_TRADES ) && OrderCloseTime()==0)
       {  
       OrderSelect(result[0], SELECT_BY_TICKET,MODE_TRADES); 
        buy_ticket= OrderSymbol();
        OrderSelect(result[1], SELECT_BY_TICKET,MODE_TRADES);
        sell_ticket=OrderSymbol();
        if(MarketInfo(buy_ticket,MODE_ASK)>=result[2] && MarketInfo(sell_ticket,MODE_BID)<=result[3])
          {  
           OrderClose(result[0],0.01,Ask,0.01,Red);
           OrderClose(result[1],0.01,Bid,0.01,Red);
           printf("有平仓实现");
          }
       }
    }

          }
  
  
 