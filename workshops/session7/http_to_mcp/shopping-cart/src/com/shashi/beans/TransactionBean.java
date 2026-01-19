package com.shashi.beans;

import java.io.Serializable;
import java.sql.Timestamp;
import java.text.SimpleDateFormat;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.TimeZone;

import com.shashi.utility.IDUtil;

@SuppressWarnings("serial")
public class TransactionBean implements Serializable {

	private String transactionId;

	private String userName;

	private Timestamp transDateTime;

	private double transAmount;

	private Timestamp getCurrentBeijingTime() {
		ZonedDateTime beijingTime = ZonedDateTime.now(ZoneId.of("Asia/Shanghai"));
		return Timestamp.from(beijingTime.toInstant());
	}

	public TransactionBean() {
		super();
		this.transactionId = IDUtil.generateTransId();
		this.transDateTime = getCurrentBeijingTime();
	}

	public TransactionBean(String userName, double transAmount) {
		super();
		this.userName = userName;
		this.transAmount = transAmount;
		this.transactionId = IDUtil.generateTransId();
		this.transDateTime = getCurrentBeijingTime();
	}

	public TransactionBean(String transactionId, String userName, double transAmount) {
		super();
		this.transactionId = transactionId;
		this.userName = userName;
		this.transAmount = transAmount;
		this.transDateTime = getCurrentBeijingTime();
	}

	public TransactionBean(String userName, Timestamp transDateTime, double transAmount) {
		super();
		this.userName = userName;
		this.transDateTime = transDateTime;
		this.transactionId = IDUtil.generateTransId();
		this.transAmount = transAmount;
	}

	public TransactionBean(String transactionId, String userName, Timestamp transDateTime, double transAmount) {
		super();
		this.transactionId = transactionId;
		this.userName = userName;
		this.transDateTime = transDateTime;
		this.transAmount = transAmount;
	}

	public String getTransactionId() {
		return transactionId;
	}

	public void setTransactionId(String transactionId) {
		this.transactionId = transactionId;
	}

	public String getUserName() {
		return userName;
	}

	public void setUserName(String userName) {
		this.userName = userName;
	}

	public Timestamp getTransDateTime() {
		return transDateTime;
	}

	public void setTransDateTime(Timestamp transDateTime) {
		this.transDateTime = transDateTime;
	}

	public double getTransAmount() {
		return transAmount;
	}

	public void setTransAmount(double transAmount) {
		this.transAmount = transAmount;
	}

}
