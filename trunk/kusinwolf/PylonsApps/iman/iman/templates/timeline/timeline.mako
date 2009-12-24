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
    Event Adder Here!
    </div>
  </div>
  </body>
</html>