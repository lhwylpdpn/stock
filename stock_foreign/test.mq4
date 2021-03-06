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
string filename_report;
int filehandle_report;
int OnInit()
  {
//--- create timer
      EventSetTimer(3);
      filename_all="balance.txt";
      filehandle_all=FileOpen(filename_all,FILE_READ|FILE_WRITE|FILE_TXT); 
      filename_report="API_report.csv";
      filehandle_report=FileOpen(filename_report,FILE_READ|FILE_WRITE|FILE_TXT);  
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
       FileClose(filehandle_report);

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
   printf(TimeMinute(TimeCurrent())==1 && is_null_file("API_callback.csv")==0);

  
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
     FileWrite(filehandle_all,string(ticket_buy)+","+string(ticket_sell)+","+string(except_buy_price)+","+string(except_sell_price)+","+string(buyprice)+","+string(sellprice)+","+string(TimeCurrent()));
     
        }

  
//+------------------------------------------------------------------+ 写入数据函数//
  void update_data(int filehandle,string name)
{   
   string str=name+","+string(iTime(name,0,0))+","+string( iOpen(name,0,0))+","+string(iHigh(name,0,0))+","+string(iLow(name,0,0))+","+string(iClose(name,0,0));
   FileWriteString(filehandle,str+"\r\n");
 }
 
//+------------------------------------------------------------------+ 获得外汇价格数据
void get_data()
{ string filename2="API_callback.csv";
                 int filehandle2=FileOpen(filename2,FILE_WRITE|FILE_CSV);  
                 
             
                update_data(filehandle2,"EURCHF...");
                update_data(filehandle2,"GBPCHF...");
                update_data(filehandle2,"AUDCHF...");
                update_data(filehandle2,"CADCHF...");
                update_data(filehandle2,"USDCHF...");
                update_data(filehandle2,"NZDCHF...");
                FileClose(filehandle2);}



//+------------------------------------------------------------------+ 平仓函数                                     
     void order_close()
  {string sep=",";                // A separator as a character
   ushort u_sep;                  // The code of the separator character
   string result[];
   string buy_ticket="";
   string sell_ticket="";
   string buy_price_active="";
   string sell_price_acitve="";
   float except_profit=0;
   FileSeek(filehandle_all,0,0);

   while(!FileIsEnding(filehandle_all))
   {           
   u_sep=StringGetCharacter(sep,0);
   //--- Split the string to substrings
         int k=StringSplit(FileReadString(filehandle_all),u_sep,result);
         
     //---balance case 1 : 超过正态比例的
      if(OrderSelect(result[0], SELECT_BY_TICKET,MODE_TRADES) && OrderCloseTime()==0 && OrderSelect(result[1], SELECT_BY_TICKET,MODE_TRADES ) && OrderCloseTime()==0 && result[2]==0 && result[3]==0)
       {  
        OrderSelect(result[0], SELECT_BY_TICKET,MODE_TRADES); 
            buy_ticket= OrderSymbol();
            buy_price_active=OrderOpenPrice();
            OrderSelect(result[1], SELECT_BY_TICKET,MODE_TRADES);
            sell_ticket=OrderSymbol();
            sell_price_acitve=OrderOpenPrice();
            except_profit=(MarketInfo(buy_ticket,MODE_BID)- float(buy_price_active) + float(sell_price_acitve) - MarketInfo(sell_ticket,MODE_ASK))/(float(buy_price_active) + float(sell_price_acitve));
            if(except_profit>=0.003)
              {
            if(OrderClose(result[0],0.01,Bid,0.01,Red)){report(result[0],result[4],result[5]);}
            if(OrderClose(result[1],0.01,Ask,0.01,Red)){report(result[1],result[4],result[5]);}
            printf("有mo limit 止盈平仓实现");
              }
         
       }
       
      //---balance case  : 止盈或者止损  
       if(OrderSelect(result[0], SELECT_BY_TICKET,MODE_TRADES) && OrderCloseTime()==0 && OrderSelect(result[1], SELECT_BY_TICKET,MODE_TRADES ) && OrderCloseTime()==0 && result[2]!=0 && result[3]!=0)
         {  OrderSelect(result[0], SELECT_BY_TICKET,MODE_TRADES); 
            buy_ticket= OrderSymbol();
            buy_price_active=OrderOpenPrice();
            OrderSelect(result[1], SELECT_BY_TICKET,MODE_TRADES);
            sell_ticket=OrderSymbol();
            sell_price_acitve=OrderOpenPrice();
            except_profit=(MarketInfo(buy_ticket,MODE_BID)- float(buy_price_active) + float(sell_price_acitve) - MarketInfo(sell_ticket,MODE_ASK))/(float(buy_price_active) + float(sell_price_acitve));
            if(except_profit>=0.002)
              {
            if(OrderClose(result[0],0.01,Bid,0.01,Red)){report(result[0],result[4],result[5]);}
            if(OrderClose(result[1],0.01,Ask,0.01,Red)){report(result[1],result[4],result[5]);}
            printf("有止盈平仓实现");
              }
            if(except_profit<=-0.002)
              {
            if(OrderClose(result[0],0.01,Bid,0.01,Red)){report(result[0],result[4],result[5]);}
            if(OrderClose(result[1],0.01,Ask,0.01,Red)){report(result[1],result[4],result[5]);}
            printf("有止损失平仓实现");
              }
         }
       
       
    } printf("balance ing");
      
          }
  
  
 void report(string orderid,string buyprice_except_open,string sellprice_except_open)
 
 {
  double open_price;
  datetime open_time;
  double close_price;
  datetime close_time;
  double profit;
  double Commission;
  double Lots;
  string stock_name;
  
  OrderSelect(orderid, SELECT_BY_TICKET);
  stock_name= OrderSymbol();
  open_price= OrderOpenPrice();
  open_time=OrderOpenTime();
  close_price=OrderClosePrice();
  close_time=OrderCloseTime();
  profit=OrderProfit();
  Commission=OrderCommission();
  Lots=OrderLots() ;
  string str=stock_name+","+string(orderid)+","+string(open_price)+","+string(open_time )+","+string(close_price)+","+string(close_time)+","+string(profit)+","+string(Commission)+","+string(Lots)+","+string(TimeCurrent())+","+buyprice_except_open+","+sellprice_except_open;
  FileWriteString(filehandle_report,str+"\r\n");

  }