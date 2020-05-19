function validate() {
  var phones = document.myForm.phones.value;
  var phoneArr = phones.split(',');
  var i;
  for (i = 0; i < phoneArr.length; i++) {
   if (!Number.isInteger(+phoneArr[i])) {
    alert("Phone provided is not an Integer: " + phoneArr[i]);
    return false;
   }
  }

  var userids = document.myForm.userids.value;
  var userArr = userids.split(',');
  var j;
  for (j = 0; j < userArr.length; j++) {
   if (!Number.isInteger(+userArr[j])) {
    alert("UserID provided is not an Integer: " + userArr[j]);
    return false;
   }
  }

  var ips = document.myForm.ips.value;
  var stripped = ips.replace(/\s+/g, '')
  var ipArr = stripped.split(',');
  var k;
  for (k = 0; k < ipArr.length; k++) {
    if (!/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipArr[k])) {
      alert("Invalid IP: " + ipArr[k]);
      return false;
    }
  }
  return(true);
}