<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Jakarta EE Test</h1>
    <p>Current time: <%= new java.util.Date() %></p>
    <p>Session ID: <%= session.getId() %></p>
</body>
</html>
