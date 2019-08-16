<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  
                xmlns:msxsl="urn:schemas-microsoft-com:xslt"
                xmlns:user="http://android.riteshsahu.com">
<xsl:template match="/">
  <html>
	  <head>
		  <style type="text/css">
		  body 
		  {
			font-family:arial,sans-serif;
			color:#000;
			font-size:13px;
			color:#333;
		  }
		  table 
		  {
			font-size:1em;
			margin:0 0 1em;
			border-collapse:collapse;
			border-width:0;
			empty-cells:show;
		  }
		  td,th 
		  {
			border:1px solid #ccc;
			padding:6px 12px;
			text-align:left;
			vertical-align:top;
			background-color:inherit;
		  }
		  th 
		  {
			background-color:#dee8f1;
		  }
		  </style>
	  </head>
	  <body>
	  <h2>SMS Messages</h2>
	  <table>
		<tr>
		  <th>Type</th>
		  <th>Number</th>
		  <th>Contact</th>
		  <th>Date</th>
		  <th>Message</th>
		</tr>
		<xsl:for-each select="messages/message">
		<tr>
		  <td>
			<xsl:if test="stat = 'Received'">
			Received
			</xsl:if>
			<xsl:if test="stat = 'Read'">
			Received
			</xsl:if>
			<xsl:if test="stat = 'Sent'">
			Sent
			</xsl:if>
		  </td>
		  <td>
		    <xsl:value-of select="telephone"/>
		  </td>
		  <td>
		    <xsl:value-of select="contact"/>
		  </td>
		  <td>
		    <span>
			<xsl:attribute name="title">
				<xsl:value-of select="dateenc" />
			</xsl:attribute>
			<xsl:value-of select="date"/>
    		    </span>
		  </td>
		  <td>
			<xsl:value-of select="text"/>
		  </td>
		</tr>
		</xsl:for-each>
	  </table>
	  </body>
  </html>
</xsl:template>
</xsl:stylesheet>