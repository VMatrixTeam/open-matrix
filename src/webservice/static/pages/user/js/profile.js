(function(){

  // run
  getAjaxDataAndRun();


  /**
   * Gets the ajax contribution map data and run.
   */
  function getAjaxDataAndRun() {

    url = '/api/1.0/profile/contribution';
    user_id = getUserIdFromLocation();

    $.get(url, {user_id: user_id}, function(result) {

      if (result.data) {
        var jsonData = convertDataToJsonFormat(result.data);
        initHeatMap(jsonData);
      }

    });

  }


  /**
   * Gets the user identifier from location.
   *
   * @return     {<string>}  The user identifier from location.
   * @author     (bukoo)
   */
  function getUserIdFromLocation() {
    var pathNameArray = window.location.pathname.split('/');
    return pathNameArray[pathNameArray.length - 1];
  }




  /**
   * Format the recieve data.
   *
   * @param      {<string>}  data    The json-string data
   * @return     {<json>}  { json data }
   */
  function convertDataToJsonFormat(data) {
    var jsondata = JSON.parse(data);
    return jsondata;
  }


  /**
   * Initial CalHeatMap with json data
   *
   * @param      {<json>}  jsonData  The json data
   */
  function initHeatMap(jsonData) {
    var startDate = getStartDateOfContribution();
    var cal = new CalHeatMap();

    cal.init({
      range: 10,
      domain: "month",
      tooltip: true,
      start: startDate,
      data: jsonData,
      dataType: 'json'
    });
  }


  /**
   * Gets the start date of contribution map.
   *
   * @return     {Date}  The start date of contribution.
   */
  function getStartDateOfContribution() {
    var startDate = new Date();
    startDate.setMonth(startDate.getMonth() - 9);
    return new Date(startDate.getFullYear(), startDate.getMonth(), 1)
  }
  
})();