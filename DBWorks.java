//package com.parser.app;

import java.io.FileReader;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Date;
import java.util.Scanner;

public class DBWorks {
	static Connection connection;
	static Statement stm;
	static String name = "";
	static double price = 0.0f;
	static double change = 0.0f;
	static int counter = 0;
	static double morningPrice;
	static int scale = (int) Math.pow(10,4);
	public static int year = 0;
	public static int month = 0;
	public static int day = 0;
	public static int hour = 0;
	public static int minute = 0;
	public static int second = 0;
	
	//�������� ������� �����
	public void getCurrTime() {
		LocalDateTime localDate = LocalDateTime.now();
		
		year = localDate.getYear();
		month = localDate.getMonthValue();
		day = localDate.getDayOfMonth();
		hour = localDate.getHour();
		minute = localDate.getMinute();
		second = localDate.getSecond();
	}
	
	
	public void morningPriceInsert() {
		ArrayList<Thread> threads = new ArrayList<>();
		ParseBCS parseBCS = new ParseBCS();
		String s = "";
			try {
				Class.forName("org.sqlite.JDBC");
				String dbase = "jdbc:sqlite:src/inv.db";
				connection = DriverManager.getConnection(dbase);
					
				} catch(Exception e) {
					System.out.println(e);
				}
					
				try {
				FileReader fileReader = new FileReader("src/links");
				Scanner scan = new Scanner(fileReader);
				counter = 0;
				while (scan.hasNextLine()) {
					s = scan.nextLine();
					final String str = s;
					Thread thread = new Thread(new Runnable() {
						public void run() {
							name = parseBCS.getName(str);
							price =  parseBCS.getPrice();
							System.out.println(name);
							System.out.println(price);
							try {
								stm = connection.createStatement();
								String sql = "insert into morningPr (a_name, a_price, day, month, year) values (?, ?, ?, ?, ?)";
								PreparedStatement preparedStatement = connection.prepareStatement(sql);
								preparedStatement.setString(1, name);
								preparedStatement.setDouble(2, price);
								preparedStatement.setInt(3, day);
								preparedStatement.setInt(4, month);
								preparedStatement.setInt(5, year);
								preparedStatement.executeUpdate();
								
								String sqlinfonow = "update infonow set morningPrice = (?), morningSum = morningPrice*amount where a_ID = (?)";
								PreparedStatement statementForInfoNow = connection.prepareStatement(sqlinfonow);

								statementForInfoNow.setDouble(1, price);
								statementForInfoNow.setDouble(2, counter);
								statementForInfoNow.executeUpdate();
									
								counter ++;
								System.out.println(counter);
									
							} catch (SQLException e) {
								e.printStackTrace();
							}
						}
						});
					threads.add(thread);
					}
				} catch (Exception e) {
					System.out.println(e);
				}
				for (int i = 0; i < threads.size(); i++) {
					threads.get(i).run();
				}
		}

	public void DBWorks() {
		//Connection connection = null;
		try {
		Class.forName("org.sqlite.JDBC");
		String dbase = "jdbc:sqlite:src/inv.db";
		connection = DriverManager.getConnection(dbase);
		
		} catch(Exception e) {
			System.out.println(e);
		}
		
		ArrayList<Thread> threads = new ArrayList<>();
		ParseBCS parseBCS = new ParseBCS();
		String s = "";
		Integer count = 0;
		
		try {
		FileReader fileReader = new FileReader("src/links");
		Scanner scan = new Scanner(fileReader);
		Scanner scanCount = new Scanner(fileReader);
		counter = 0;
		while (scan.hasNextLine()) {
			s = scan.nextLine();
			final String str = s;
			//final Connection thrConnection = connection;
			Thread thread = new Thread(new Runnable() {
				public void run() {
					name = parseBCS.getName(str);
					price =  parseBCS.getPrice();
					change =  parseBCS.getChange();
					System.out.println(name);
					System.out.println(price);
					System.out.println(change);
					try {
						Date date = new Date();
						LocalDateTime localDate = LocalDateTime.now();
						
						stm = connection.createStatement();
						String sql = "insert into inv (datetime, a_name, a_price, a_change, year, month, day, hour, minute, second) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
						PreparedStatement preparedStatement = connection.prepareStatement(sql);
						preparedStatement.setInt(1, (int) date.getTime());
						preparedStatement.setString(2, name);
						preparedStatement.setDouble(3, price);
						preparedStatement.setDouble(4, change);
						preparedStatement.setInt(5, year);
						preparedStatement.setInt(6, month);
						preparedStatement.setInt(7, day);
						preparedStatement.setInt(8, hour);
						preparedStatement.setInt(9, minute);
						preparedStatement.setInt(10, second);
						//System.out.println(date.getYear());
						int rows = preparedStatement.executeUpdate();
						
						counter ++;
						System.out.println(counter);
						
						String sqlinfonow = "update infonow set a_price = (?), change = (?), morningPrice = (?), morningSum = morningPrice*amount where a_ID = (?)";
						PreparedStatement statementForInfoNow = connection.prepareStatement(sqlinfonow);
						statementForInfoNow.setDouble(1, price);
						statementForInfoNow.setDouble(2, change);
						
						morningPrice = price/(1 + change/100);
						morningPrice = Math.ceil(morningPrice * scale) / scale;
						
						statementForInfoNow.setDouble(3, morningPrice);
						
						//statementForInfoNow.setDouble(4, morningPrice);
						statementForInfoNow.setDouble(4, counter);
						int rows1 = statementForInfoNow.executeUpdate();
						
						String sqlinfonowGetSum = "update infonow set a_sum = a_price*amount where a_ID = (?)";
						PreparedStatement statementForInfoNowGetSum = connection.prepareStatement(sqlinfonowGetSum);
						statementForInfoNowGetSum.setDouble(1, counter);
						int rows2 = statementForInfoNowGetSum.executeUpdate();
						//System.out.println(rows);
					} catch (SQLException e) {
						e.printStackTrace();
					}
				}
			});
			threads.add(thread);
			}
		} catch (Exception e) {
			System.out.println(e);
		}
		for (int i = 0; i < threads.size(); i++) {
			threads.get(i).run();
		}
	}
	
	
	
}
