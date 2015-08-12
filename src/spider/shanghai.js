function strEncode(str) {
  var strEncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
  var out, i, len;
  var c1, c2, c3;
  len = str.length;
  i = 0;
  out = "";
  while (i < len) {
    c1 = str.charCodeAt(i++) & 255;
    if (i == len) {
      out += strEncodeChars.charAt(c1 >> 2);
      out += strEncodeChars.charAt((c1 & 3) << 4);
      out += "==";
      break;
    }
    c2 = str.charCodeAt(i++);
    if (i == len) {
      out += strEncodeChars.charAt(c1 >> 2);
      out += strEncodeChars.charAt(((c1 & 3) << 4) | ((c2 & 240) >> 4));
      out += strEncodeChars.charAt((c2 & 15) << 2);
      out += "=";
      break;
    }
    c3 = str.charCodeAt(i++);
    out += strEncodeChars.charAt(c1 >> 2);
    out += strEncodeChars.charAt(((c1 & 3) << 4) | ((c2 & 240) >> 4));
    out += strEncodeChars.charAt(((c2 & 15) << 2) | ((c3 & 192) >> 6));
    out += strEncodeChars.charAt(c3 & 63);
  }
  return out;
}
function strDecode(str) {
  var strDecodeChars = new Array(-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1, -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1, -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1);
  var c1, c2, c3, c4;
  var i, len, out;
  len = str.length;
  i = 0;
  out = "";
  while (i < len) {
    /* c1 */
    do {
      c1 = strDecodeChars[str.charCodeAt(i++) & 255];
    } while (i < len && c1 == -1);
    if (c1 == -1) {
      break;
    }
    /* c2 */
    do {
      c2 = strDecodeChars[str.charCodeAt(i++) & 255];
    } while (i < len && c2 == -1);
    if (c2 == -1) {
      break;
    }
    out += String.fromCharCode((c1 << 2) | ((c2 & 48) >> 4));
    /* c3 */
    do {
      c3 = str.charCodeAt(i++) & 255;
      if (c3 == 61) {
        return out;
      }
      c3 = strDecodeChars[c3];
    } while (i < len && c3 == -1);
    if (c3 == -1) {
      break;
    }
    out += String.fromCharCode(((c2 & 15) << 4) | ((c3 & 60) >> 2));
    /* c4 */
    do {
      c4 = str.charCodeAt(i++) & 255;
      if (c4 == 61) {
        return out;
      }
      c4 = strDecodeChars[c4];
    } while (i < len && c4 == -1);
    if (c4 == -1) {
      break;
    }
    out += String.fromCharCode(((c3 & 3) << 6) | c4);
  }
  return out;
}
function utf16to8(str) {
  var out, i, len, c;
  out = "";
  len = str.length;
  for (i = 0; i < len; i++) {
    c = str.charCodeAt(i);
    if ((c >= 1) && (c <= 127)) {
      out += str.charAt(i);
    } else {
      if (c > 2047) {
        out += String.fromCharCode(224 | ((c >> 12) & 15));
        out += String.fromCharCode(128 | ((c >> 6) & 63));
        out += String.fromCharCode(128 | ((c >> 0) & 63));
      } else {
        out += String.fromCharCode(192 | ((c >> 6) & 31));
        out += String.fromCharCode(128 | ((c >> 0) & 63));
      }
    }
  }
  return out;
}
function utf8to16(str) {
  var out, i, len, c;
  var char2, char3;
  out = "";
  len = str.length;
  i = 0;
  while (i < len) {
    c = str.charCodeAt(i++);
    switch (c >> 4) {
      case 0:
      case 1:
      case 2:
      case 3:
      case 4:
      case 5:
      case 6:
      case 7: // 0xxxxxxx
        out += str.charAt(i - 1);
        break;
      case 12:
      case 13: // 110x xxxx? 10xx xxxx
        char2 = str.charCodeAt(i++);
        out += String.fromCharCode(((c & 31) << 6) | (char2 & 63));
        break;
      case 14: // 1110 xxxx?10xx xxxx?10xx xxxx
        char2 = str.charCodeAt(i++);
        char3 = str.charCodeAt(i++);
        out += String.fromCharCode(((c & 15) << 12) | ((char2 & 63) << 6) | ((char3 & 63) << 0));
        break;
    }
  }
  return out;
}

function URLencode(sStr) {
  return escape(sStr).replace(/\+/g, '%2B').replace(/\"/g,'%22').replace(/\'/g, '%27').replace(/\//g,'%2F');
}

function showMenus(page,siteCode){
  //var page = URLencode(strEncode(utf16to8(page.toString())));
  //var siteCode = URLencode(strEncode(utf16to8(siteCode.toString())));
  var searchWord = URLencode(strEncode(utf16to8(document.getElementById('searchWordKey').value)));
  //alert(document.getElementById('searchWordKey').value);
  //window.location.href="?page="+page+"&isBusiness="+urlPara+"&siteCode="+siteCode+"&status=code" ;
  //window.location.href="load.loadPage.d?page="+page+"&siteCode="+siteCode+"&searchWord="+searchWord ;
  window.open('load.loadPage.d?page='+page+'&siteCode='+siteCode+'&searchWord='+searchWord+'','','resizable=1,scrollbars=yes,Height=600,Width=780,left=120,top=150');return false;
  return false;
}
(function showMenus2(id,detailChannel,urlMenuId){
  var id= URLencode(strEncode(utf16to8(id)));
  var detailChannel = URLencode(strEncode(utf16to8(detailChannel)));
  var urlMenuId = URLencode(strEncode(utf16to8(urlMenuId )));
  //return id;
  return 'load.loadPage.d?newsid='+id+'&page=detail_iframe.xml&siteCode=sdnw&detailChannel='+detailChannel+'&urlMenuId='+urlMenuId+''

  //window.location.href="?page="+page+"&isBusiness="+urlPara+"&siteCode="+siteCode+"&status=code" ;
  //window.location.href="load.loadPage.d?page="+page+"&siteCode="+siteCode+"&searchWord="+searchWord ;
  //window.open('load.loadPage.d?newsid='+id+'&page=detail_index.xml&siteCode=sdnw&detailChannel='+detailChannel+'&urlMenuId='+urlMenuId+'','','resizable=1,scrollbars=yes,Height=700,Width=980,left=120,top=150');return false;
  //return false;
})
