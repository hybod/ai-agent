package com.shashi.srv;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import com.shashi.beans.ProductBean;
import com.shashi.service.impl.ProductServiceImpl;

@WebServlet("/ListProducts")
public class ListProducts extends HttpServlet {
	private static final long serialVersionUID = 1L;

	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		
		response.setContentType("application/json");
		response.setCharacterEncoding("UTF-8");
		
		ProductServiceImpl productService = new ProductServiceImpl();
		List<ProductBean> products = productService.getAllProducts();
		
		PrintWriter out = response.getWriter();
		out.print("[");
		
		for (int i = 0; i < products.size(); i++) {
			ProductBean product = products.get(i);
			
			out.print("{");
			out.print("\"prodId\":\"" + product.getProdId() + "\",");
			out.print("\"prodName\":\"" + escapeJson(product.getProdName()) + "\",");
			out.print("\"prodType\":\"" + escapeJson(product.getProdType()) + "\",");
			out.print("\"prodInfo\":\"" + escapeJson(product.getProdInfo()) + "\",");
			out.print("\"prodPrice\":" + product.getProdPrice() + ",");
			out.print("\"prodQuantity\":" + product.getProdQuantity());
			out.print("}");
			
			if (i < products.size() - 1) {
				out.print(",");
			}
		}
		
		out.print("]");
		out.flush();
	}
	
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doGet(request, response);
	}
	
	private String escapeJson(String str) {
		if (str == null) return "";
		return str.replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r");
	}
}
