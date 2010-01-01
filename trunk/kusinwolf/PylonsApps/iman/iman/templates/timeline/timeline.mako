<html>
  <head>
    <title>Community Timeline</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8" />
    
    <link rel="stylesheet" type="text/css" href="../css/timeline.css">
    <link rel="stylesheet" type="text/css" href="../../css/timeline.css">
    <link rel="stylesheet" type="text/css" href="http://yui.yahooapis.com/2.7.0/build/base/base-min.css">
    
    <!-- Load the Timeline library after reseting the fonts, etc -->
    <script src="http://static.simile.mit.edu/timeline/api-2.3.0/timeline-api.js?bundle=true" type="text/javascript"></script>
    
    <!-- Since we don't have our own server, we do something tricky and load our data here as if it were a library file -->
    <script src="../js/timeline.js" type="text/javascript"></script>
    
    <script>        
      var tl;
      function onLoad() {
          var tl_el = document.getElementById("tl");
          var eventSource1 = new Timeline.DefaultEventSource();
          
          var theme1 = Timeline.ClassicTheme.create();
          theme1.autoWidth = true; // Set the Timeline's "width" automatically.
                                   // Set autoWidth on the Timeline's first band's theme,
                                   // will affect all bands.
          theme1.timeline_start = new Date(Date.UTC(1998, 0, 1)); // When to begin
          theme1.timeline_stop  = new Date(Date.UTC(2011, 0, 1)); // When to end
          
          var d = Timeline.DateTime.parseGregorianDateTime("2001") // center on date
          var bandInfos = [
              Timeline.createBandInfo({
                  width:          "20%", // set to a minimum, autoWidth will then adjust
                  intervalUnit:   Timeline.DateTime.DAY, // YEAR, DECADE, DAY
                  intervalPixels: 200,
                  eventSource:    eventSource1,
                  theme:          theme1,
                  layout:         'original',  // original, overview, detailed
              }),
              Timeline.createBandInfo({
                  width:          "50%", // set to a minimum, autoWidth will then adjust
                  intervalUnit:   Timeline.DateTime.MONTH, // YEAR, DECADE, DAY
                  intervalPixels: 200,
                  eventSource:    eventSource1,
                  theme:          theme1,
                  layout:         'original',  // original, overview, detailed
              }),
              Timeline.createBandInfo({
                  width:          "30%", // set to a minimum, autoWidth will then adjust
                  intervalUnit:   Timeline.DateTime.YEAR, // YEAR, DECADE, DAY
                  intervalPixels: 300,
                  eventSource:    eventSource1,
                  theme:          theme1,
                  layout:         'detailed',  // original, overview, detailed
              })
          ];
          
          // create the Timeline
          tl = Timeline.create(tl_el, bandInfos, Timeline.HORIZONTAL);
          
          var url = '.'; // The base url for image, icon and background image
                         // references in the data
          eventSource1.loadJSON(timeline_data, url); // The data was stored into the 
                                                     // timeline_data variable.
          tl.layout(); // display the Timeline
      }
      
      var resizeTimerID = null;
      function onResize() {
          if (resizeTimerID == null) {
              resizeTimerID = window.setTimeout(function() {
                  resizeTimerID = null;
                  tl.layout();
              }, 500);
          }
      }
      
      var oldFillInfoBubble = Timeline.DefaultEventSource.Event.prototype.fillInfoBubble;
      
      Timeline.DefaultEventSource.Event.prototype.fillInfoBubble =
        function(elmt, theme, labeller) {
          //oldFillInfoBubble.call(this, elmt, theme, labeller);
          var doc = elmt.ownerDocument;
        
          var title = this.getText();
          var link = this.getLink();
          var image = this.getImage();
          
          if (image != null) {
              var img = doc.createElement("img");
              img.src = image;
              
              theme.event.bubble.imageStyler(img);
              elmt.appendChild(img);
          }
          
          var divTitle = doc.createElement("div");
          var textTitle = doc.createTextNode(title);
          if (link != null) {
              var a = doc.createElement("a");
              a.href = link;
              a.appendChild(textTitle);
              divTitle.appendChild(a);
          } else {
              divTitle.appendChild(textTitle);
          }
          theme.event.bubble.titleStyler(divTitle);
          elmt.appendChild(divTitle);
          
          var divBody = doc.createElement("div");
          this.fillDescription(divBody);
          theme.event.bubble.bodyStyler(divBody);
          elmt.appendChild(divBody);
          
          var divTime = doc.createElement("div");
          this.fillTime(divTime, labeller);
          theme.event.bubble.timeStyler(divTime);
          elmt.appendChild(divTime);
        }
   </script>
  </head>
  <body bgcolor="EEEEEE" onload="onLoad();" onresize="onResize();">
  <div id="doc3" class="yui-t7">
    <div id="hd" role="banner">
      <h1>Gaming Community Timeline</h1>
      <p>Scroll by dragging the timeline. Click on an event to see its details. Add an event to the timeline at the bottom.</p>
    </div>
    <div id="bd" role="main">
      <div class="yui-g">
        <div id='tl'>
        </div>
      </div>
    </div>
    <div id="ft" role="contentinfo">
    <center>
    <h1>Add an Event!</h1>
    <table border='0'>
    ${h.form(h.url_for(action="event_create"), method="post")}
      <tr><td>Title</td><td>${h.textarea(name="title", rows=1, cols=80, content="")}</td></tr>
      <tr><td>Description</td><td>${h.textarea(name="description", rows=7, cols=80, content="")}</td></tr>
      <tr><td>Start Date</td><td>Year: ${h.select("start_year", None, c.years)} Month: ${h.select("start_month", None, c.months)} Day: ${h.select("start_day", None, c.days)} Hour: ${h.select("start_hour", None, c.hours)} Minute: ${h.select("start_minute", None, c.minutes)} Second: ${h.select("start_second", None, c.seconds)}</td></tr>
      <tr><td>End Date</td><td>Year: ${h.select("end_year", None, c.years)} Month: ${h.select("end_month", None, c.months)} Day: ${h.select("end_day", None, c.days)} Hour: ${h.select("end_hour", None, c.hours)} Minute: ${h.select("end_minute", None, c.minutes)} Second: ${h.select("end_second", None, c.seconds)}<br />* (Not required for single point date, only required for duration of time)</td></tr>
      <tr><td>Over a Peroid of time?</td><td>${h.select("isDuration", None, c.duration)}<br />* (If the event spans across the start and end dates)</td></tr>
      <tr><td>Image</td><td>${h.textarea(name="image", rows=1, cols=80, content="")}<br />* (a link to an image will work)</td></tr>
      <tr><td>Link</td><td>${h.textarea(name="link", rows=1, cols=80, content="")}<br />* (a link when the title is clicked on in the details popup)</td></tr>
      <tr><td>Title Text Color</td><td>${h.textarea(name="textColor", rows=1, cols=5, content="")}<br />* (Hex value of the color you desire, Example: "0F32AB")</td></tr>
      <tr><td>Bar Color</td><td>${h.textarea(name="color", rows=1, cols=5, content="")}<br />* (Hex value of the color you desire, Example: "0F32AB")</td></tr>
      <tr><td>Icon</td><td>${h.select("icon", None, c.icons)}<br />* (What picture shows up on the overview next to the title)</td></tr>
      <tr><td>Caption</td><td>${h.textarea(name="caption", rows=1, cols=80, content="")}<br />* (Popup text when hovering over the title in the overview)</td></tr>
      <tr><td colspan=2 align=center>${h.submit("Submit", "Add Event")}</td></tr>
    ${h.end_form()}
    </table>
    </center>
    </div>
  </div>
  </body>
</html>