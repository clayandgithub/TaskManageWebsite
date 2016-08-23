function writeCalendar()
{
	function changeColor(index) {
	document.getElementById(index).bgColor="gray";
}
function recoverColor(index) {
	document.getElementById(index).bgColor="yellow";
}
monthnames = new Array("1月","2月","3月","4月","5月","6月","7月","8月","10月","11月","12月"); 

var linkcount=0;

function addlink(month, day, href) {
var entry = new Array(3);
entry[0] = month;
entry[1] = day;
entry[2] = href;
this[linkcount++] = entry;
}

Array.prototype.addlink = addlink;
linkdays = new Array();

monthdays = new Array(12);
monthdays[0]=31;
monthdays[1]=28;
monthdays[2]=31;
monthdays[3]=30;
monthdays[4]=31;
monthdays[5]=30;
monthdays[6]=31;
monthdays[7]=31;
monthdays[8]=30;
monthdays[9]=31;
monthdays[10]=30;
monthdays[11]=31;

todayDate=new Date();
thisday=todayDate.getDay();
thismonth=todayDate.getMonth();
thisdate=todayDate.getDate();
thisyear=todayDate.getFullYear();

if (((thisyear % 4 == 0) && !(thisyear % 100 == 0))||(thisyear % 400 == 0)) monthdays[1]++;

startspaces = thisdate;
if(startspaces > 7) startspaces %= 7;
startspaces = thisday - startspaces + 1;
if(startspaces < 0) startspaces += 7;

document.write("<table  class = 'left_div' style = 'border:0px;'>");
document.write("<tr><td colspan=7>");
document.write("<center>" + thisyear +"年"+monthnames[thismonth-1]);
document.write("</center></td></tr>");
document.write("<tr>");
document.write("<td align=center'>日</td>");
document.write("<td align=center>一</td>");
document.write("<td align=center>二</td>");
document.write("<td align=center>三</td>");
document.write("<td align=center>四</td>");
document.write("<td align=center>五</td>");
document.write("<td align=center>六</td>"); 
document.write("</tr>");
document.write("<tr>");
var i=0;
for (s=0;s<startspaces;s++) {
document.write("<td>&nbsp</td>");
}
count=1;
while (count <= monthdays[thismonth]) {
	for (b = startspaces;b<7;b++) {
		linktrue=false;
		document.write("<td id='tt" + ++i + "'>");
		if (count==thisdate) {
			document.write("<span style = 'color:#000;border:2px solid #F00;border-radius:4px;'>");
			document.write(count);
			document.write("</span>");
		}
		else if (count <= monthdays[thismonth]) {
			document.write(count);
		}
		else {
			document.write("&nbsp");
		}
		if (linktrue)
			document.write("</a>");
		document.write("</td>");
		count++;
	}
		document.write("</tr>");
		document.write("<tr>");
		startspaces=0;
}
document.write("</table>");
}
