//package com.parser.app;

import java.time.LocalDateTime;
import java.util.TimerTask;
import java.util.Timer;

public class Main {
	

	public static void main(String[] args) {
		try{
			DBWorks dbworks = new DBWorks();
			while(true) {
				dbworks.getCurrTime();
			
				// цена утром
				if ((DBWorks.hour == 23) & (DBWorks.minute == 33) & (DBWorks.second == 0)){
					dbworks.morningPriceInsert();
				}
			
				// получем инфу в 8, 12, 16, 20, 00 часов
				if (((DBWorks.hour == 8) & (DBWorks.minute == 0) & (DBWorks.second == 0)) || 
						((DBWorks.hour == 12) & (DBWorks.minute == 0) & (DBWorks.second == 0)) ||
						((DBWorks.hour == 16) & (DBWorks.minute == 0) & (DBWorks.second == 0)) || 
						((DBWorks.hour == 20) & (DBWorks.minute == 0) & (DBWorks.second == 0)) || 
						((DBWorks.hour == 0)) & (DBWorks.minute == 0) & (DBWorks.second == 0)) {
							dbworks.DBWorks();
							}
				}
			
			
			} catch(Exception e){
				e.printStackTrace();
		}
	}

}
