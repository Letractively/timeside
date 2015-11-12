# Note: This project has been moved to [yomguy/TimeSide on GitHub](https://github.com/yomguy/TimeSide). #

**Table of contents**


## Introduction ##

The TimeSide UI features a powerful DHTML-based interactive player with [time marking](#Markers_control_and_management.md) capabilities. It can be used as a standalone client-side component. As of June 2011, it is supported in all major browsers: Internet Explorer (IE) 7+, Firefox (FF) 3.5+ and Chrome 9+

The player can be created and manipulated using a JavaScript [object oriented](http://ejohn.org/blog/simple-javascript-inheritance/)  API,
customized using [CSS and skins](#CSS_and_skins.md), and [dynamically resized](#Dynamic_resizing.md):

| <img src='http://files.parisson.com/telemeta/playerSchema.png' /> | <ol><li>play<li>pause<li>rewind (move pointer to previous marker <br> - or sound start if no marker)<li>forward (move pointer to next marker <br> - or sound end if no marker)<li>add marker (at sound - i.e., pointer - position)<li>volume (toggles volume on/off)<li>volume bar (sets volume level)<li>wait panel (visible only on sound loading/buffering or image refreshing) </tbody></table>

See <a href='http://code.google.com/p/timeside/wiki/TimeSideGadgetUIPlayer'>here</a> for a live example with enhanced marker objects, as explained in the <a href='#Markers_control_and_management.md'>Marker section</a>.<br>
<br>
For reference, here is the structure of the dynamically generated markup structure:<br>
<br>
<h3>Markup structure</h3>

<pre><code>&lt;div class="ts-ruler"&gt;           &lt;!-- upper &lt;div&gt; (ruler) --&gt;<br>
    &lt;svg class="ts-ruler-lines"&gt;        &lt;!-- The ruler lines --&gt;<br>
    &lt;a class="ts-pointer"&gt;&lt;span/&gt;&lt;/a&gt;   &lt;!-- pointer label --&gt;<br>
    &lt;a class="ts-marker"&gt;&lt;span/&gt;&lt;/a&gt;    &lt;!-- marker label --&gt;<br>
    ...<br>
&lt;/div&gt;<br>
&lt;div class="ts-wave"&gt;            &lt;!-- central &lt;div&gt; (wave) --&gt;<br>
    &lt;div class="image-canvas"&gt;         &lt;!-- svgs container. Should not be modified by custom css--&gt;<br>
        &lt;svg class="ts-pointer-canvas"&gt;    &lt;!-- Pointer vertical line --&gt;<br>
        &lt;svg class="ts-marker-canvas"&gt;     &lt;!-- Marker vertical line --&gt;<br>
        ... <br>
    &lt;/div&gt;<br>
    &lt;div class="image-container"&gt;      &lt;!-- wave image container. Should not be modified by custom css--&gt;<br>
        &lt;img class="image"/&gt;              &lt;!-- wave image. Should not be modified by custom css--&gt;<br>
    &lt;/div&gt;<br>
&lt;/div&gt;<br>
&lt;div class="ts-control"&gt;         &lt;!-- bottom &lt;div&gt; (control) --&gt;<br>
    &lt;a class='ts-play ts-button'&gt;&lt;/a&gt;<br>
    &lt;a class='ts-pause ts-button'&gt;&lt;/a&gt;<br>
    &lt;a class='ts-rewind ts-button'&gt;&lt;/a&gt;<br>
    &lt;a class='ts-forward ts-button'&gt;&lt;/a&gt;<br>
    &lt;a class='ts-set-marker ts-button'&gt;&lt;/a&gt;<br>
    &lt;a class='ts-volume-speaker ts-button'&gt;&lt;/a&gt;<br>
    &lt;div class='ts-volume-wrapper-div'&gt;<br>
        &lt;a class='ts-volume-bar-container'&gt;<br>
            &lt;span class='ts-volume-bar'&gt;&lt;/span&gt;<br>
        &lt;/a&gt;<br>
    &lt;/div&gt;<br>
    &lt;div class='ts-wait'&gt;&lt;/div&gt;<br>
&lt;/div&gt;<br>
&lt;!-- Note that all svg's might be vml object if svg is not supported (thanks to Raphael library, see doc below --&gt;<br>
</code></pre>

<h3>Setup and Dependencies</h3>

The easiest way to get started is to copy the content of the TimeSide UI package on your webserver, for example in a timeside-ui/ folder.<br>
<br>
A few external JavaScript packages are required, and must be loaded before TimeSide UI:<br>
<br>
<ul><li><a href='http://jquery.com/'>jQuery</a> >= 1.6<br>
</li><li><a href='http://www.schillmania.com/projects/soundmanager2/'>SoundManager 2</a> >= 2.97</li></ul>

For conveniency these libraries are bundled in the TimeSide UI package. So settings things up<br>
should be easily done within the <code>&lt;head/&gt;</code> tag:<br>
<br>
<pre><code>&lt;script type="text/javascript" src="timeside-ui/lib/jquery-1.6.min.js"&gt;&lt;/script&gt; <br>
&lt;script type="text/javascript" src="timeside-ui/lib/soundmanager2-nodebug-jsmin.js"&gt;&lt;/script&gt; <br>
&lt;script type="text/javascript" src="timeside-ui/timeside.js"&gt;&lt;/script&gt; <br>
</code></pre>

Of course, you are free to load your preferred versions of the dependencies, provided<br>
they meet the requirements outlined above.<br>
<br>
<font color='#666'>As svg is not supported in all browsers (specifically, IE7 and IE8), the TimeSide library first checks for svg support and, in negative case, loads and delegates the <a href='http://raphaeljs.com/reference.html'>Raphael Graphics Library</a> for building vml graphics (an old format of IE). The library is also bundled in in the TimeSide UI package</font>

<h2>Getting started</h2>
Few notes before getting started: the whole TimeSide UI API resides under the <code>Timeside</code> JavaScript global object (The goal is to strictly avoid polluting the global namespace). To initialize the TimeSide player it is sufficient to call the method <code>Timeside.load</code> as described below. The method is executed once the document is ready, so that it can be safely called everywhere in the code; it first loads all necessary timeside scripts (including Raphael library if necessary) whose path is retrieved by searching the src attribute of the <code>timeside.js</code> <code>&lt;script&gt;</code>: therefore, move your timeside-ui/ folder wherever you want but do not move any JavaScript file within it!<br>
<br>
SoundManager has properties which configure debug mode, flash movie path and other behaviours. At minimum, the soundManager.url property must be assigned a path used to look for the necessary flash movie. Therefore, before loading the player it is necessary to write something like:<br>
<pre><code>&lt;script type="text/javascript"&gt;<br>
   soundManager.url = '/path/to/swfs/';  // path (directory) where SM2 .SWF files will be found.<br>
&lt;/script&gt;<br>
</code></pre>
where '/path/to/swfs/' is the path of the '/swf' folder inside the downloaded TimeSide package. Please refer to <a href='http://www.schillmania.com/projects/soundmanager2/doc/#sm-config'>soundManager configuration</a> for more properties.<br>
<br>
<font color='#666'>We are aware that in JavaScript Integer and Float types are treated as a numeric type. However, in the remainder of the document (especially in code examples) we will avoid formality in order to be exhaustive. Therefore, when possible we will use the notations <code>int</code> and <code>float</code></font>

<h3>A simple (static) player</h3>
A simple graphical player can be embedded in your HTML page by calling, e.g.:<br>
<pre><code>Timeside.load({<br>
    container: "#player", <br>
    sound: "/path-to/my_sound.mp3",<br>
    soundDuration: 149264,<br>
    soundImage: "/path-to/my_image.png",<br>
   }<br>
);<br>
</code></pre>

where:<br>
<br>
<pre><code> container: string or object<br>
</code></pre>
<blockquote>is the player containing <code>&lt;div&gt;</code>, in one of the following formats<br>
<ol><li>jQuery string format, e.g.: <code>'#player'</code>
</li><li>jQuery element, e.g.: <code>jQuery('#player')</code>
</li><li>HTML DOMelement, e.g.: <code>document.getElementById('player')</code></li></ol></blockquote>

<blockquote><font color='#666'>Note that<br>
<ol><li><b><code>container</code></b> must be already attached to the document, either by means of standard html or dynamically with JavaScript. The content of <b><code>container</code></b>, if any, will be erased and replaced by the player elements.<br>
</li><li>At first, we suggest to use one of the TimeSide <a href='#CSS_and_skins.md'>stylesheets</a> to properly display the player. In this case, the markup structure within <code>container</code> must be embedded in (not necessarily as a child of) a <code>&lt;div/&gt;</code> of class "ts-player"<br>
</font><i></li></ol></blockquote></i>

<pre><code> sound: string or object<br>
</code></pre>
<blockquote>is the sound to be played, in one of the following formats:<br>
<ol><li>string denoting the url of the sound,<br>
</li><li>the sound object created via <code>soundManager.createSound</code> function (see  <a href='http://www.schillmania.com/projects/soundmanager2/doc/'>SoundManager documentation</a> for details)<br>
</li><li>the argument to <code>soundManager.createSound</code> function (JavaScript object). Note that the object has two minimum required fields, id and url, both strings. It is useful to specify some additional properties of the sound object, e.g.:<br>
<pre><code>       {<br>
         id: 'mysound',              //required<br>
         url: 'path_to/my_url.mp3',  //required<br>
         multiShot: false,           // avoid sound "restart" or "chorus" when played multiple times<br>
                                     // (by default it is true)<br>
       }<br>
</code></pre>
</li></ol><blockquote>Please refer to the section <code>"SoundManager Global Sound Object Defaults"</code> <a href='http://www.schillmania.com/projects/soundmanager2/doc/'>of this page</a> for a list of available properties. Adding properties denoting functions fired while playing should be done with care: first, some of them are already attached to the sound object by the TimeSide API internally (eg, <code>whileplaying</code>, <code>onfinish</code>), thus, depending on the sound object behaviour (not tested) they could be overridden or interfere with the player performances. Second, the TimeSide player has a lot of <a href='#Event_listening_and_notification.md'>notification methods</a> which cover almost all user needs.<br><br>Finally, note that in the first case, i.e. when the parameter <code>sound</code> is an url string, the argument of <code>soundManager.createSound</code> function defaults to:<br>
<pre><code>     {<br>
        id: 'ts-sound',<br>
        autoLoad: false,<br>
        url: sound,<br>
        multiShot: false<br>
     }<br>
</code></pre></blockquote></blockquote>

<pre><code> duration: int<br>
</code></pre>
<blockquote>is the sound duration <b>in milliseconds</b>. A typical example is t calculate it server-side by means of TimeSide analysers and sent to the page. This parameter is mandatory, otherwise the sound object should be first loaded in order to know its duration, and then the player (and thus, the HTML page) rendered and displayed.</blockquote>

<blockquote>In any case, it is possible to query the sound object (at the cost of slowing down page rendering), but in this case the sound object must be preloaded:<br>
<pre><code>    var config = {...}; //the object that will be passed as argument to Timeside.load<br>
                        //populated with our properties  <br>
    soundManager.createSound({<br>
        id: 'my_id',<br>
        url : 'path_to/my_url.mp3',<br>
        autoLoad: true,<br>
        onload = function(){<br>
            var d = this.duration; //this refers to the sound object<br>
                                   //note that duration might be zero or undefined if the load failed <br>
            config.sound = this; //set the sound (already loaded)<br>
            config.soundDuration = d; //set the duration <br>
            TimeSide.load(config);<br>
        }<br>
    })<br>
</code></pre></blockquote>

<pre><code> soundImage: string<br>
</code></pre>
<blockquote>is the wave image URL, in string format</blockquote>

<h3>A more complex (dynamic) player</h3>

To fully take advantage of all player capabilities (e.g., dynamic resizing, control over the loading process, marker management, player management once loaded) we can create a player by calling:<br>
<br>
<pre><code>Timeside.load({<br>
    container:        "#player", <br>
    sound:            "/path-to/my_sound.mp3"<br>
    soundDuration:    149264,<br>
    soundImage:       function(width,height){...},<br>
    imageSize:        {width: 170,height: 30},       //optional<br>
    markersArray:     [marker_1, ...., marker_N],    //optional<br>
    newMarker:        function(offset){...},         //optional<br>
    onError:          function(errorMsgString){...}, //optional<br>
    onReady:          function(player){...},         //optional<br>
    onReadyWithImage: function(player){...},         //optional<br>
    messages:         {loading: 'loading', ...}      //optional<br>
   }<br>
);<br>
</code></pre>

where <b><code>container</code></b>, <b><code>sound</code></b> and <b><code>duration</code></b> are specified above, and:<br>
<br>
<pre><code> soundImage: string or function<br>
</code></pre>
<blockquote>is the wave image URL. It can be:<br>
<ol><li>a string (see abve), to denote a static image<br>
</li><li>a callback (JavaScript function). The callback takes as argument two numbers, the width and height of the <code>&lt;div/&gt;</code> housing the new image and must return the image URL in string format. This allows, e.g., to perform high quality server-side resizing/resampling by queryng, e.g., the TimeSide graphers for the sound image with given width and height. Obviously, a callback returning a constant string, such as <code>function(w,h){return 'mywave.png';}</code> has the same effect than specifying 'mywave.png' as <b>soundImage</b> parameter: actually, this parameter will override the function <code>player.imageCallback</code> (see <a href='#Dynamic_resizing.md'>dynamic resizing</a> and <a href='#Layout.md'>player layout methods</a>): if <b><code>soundImage</code></b> is specified as string, it will be converted to a function always returning <b><code>soundImage</code></b>, regardeless of the parameters width and height</li></ol></blockquote>

<pre><code> imageSize: object<br>
</code></pre>
<blockquote>is a JavaScript object with two properties, 'width' and 'height', which specifiy the initial default size <b>of the wave <code>&lt;div&gt;</code></b>. Any other value (undefined, null, non-JavaScript object) will be ignored and has no effect on the initial size (which will be thus calculated according to the css rules). Accordingly, an object with only one property 'width' or 'height' will skip the missing one and set only the existing one.</blockquote>

<blockquote><font color='#666'>Note: Usually the player is embedded in a web page with components interacting with each other. Thus it might be more convenient to skip this parameter and specify player dimensions properties in a separate stylesheet (see <a href='#CSS_and_skins.md'>CSS and skins</a> section for details) as for all other page elements. Keep in mind however, that if no css at all is provided on the player elements, <b><code>imageSize</code></b> must be specified to properly display at least the wave image</font><i></blockquote></i>

<pre><code> markersArray: Array<br>
</code></pre>
<blockquote>is an array of markers to be visualized on the player ruler when the player loads. In the remainder of this doc, a marker is a JavaScript object with only one required key, <code>offset</code>, which indicates the marker time position as a float in the format <i>seconds.milliseconds</i>, e.g.:<br>
<pre><code>{offset: 57.300156}<br>
</code></pre>
If <b><code>markersArray</code></b> is empty, undefined or any other non-array value, no marker will be displayed at startup.</blockquote>

<blockquote><font color='#666'>When the player is fully loaded, markers are stored in an Array-like object (markerMap) instance of <a href='#Inhertance_Structure.md'>TimesideArray</a>. The map is sorted in ascending order according to markers offset. An (unique) id is automatically set on each marker in order to manage the case of two markers with the same offset (see notes on <b>newMarker</b> below for details). Adding, removal and getting marker elements is performed via a <a href='http://en.wikipedia.org/wiki/Binary_search_algorithm'>binary search algorithm</a> which is substantially faster as the number of markers N grows large (log2(N) maximum iterations)</font><i></blockquote></i>

<pre><code> newMarker: boolean or function<br>
</code></pre>
<blockquote>controls whether new markers can be added to the player (and graphically on the player ruler). Possible values are:<br>
</blockquote><ul><li>false: no marker can be added. The 'add marker' button will be hidden on the player control<br>
</li><li>true or function: markers can be added. The 'add marker' button will be visible on the player control<br>
<ol><li>If true, when a new marker is added, the function <pre><code>player.newMarker(player_current_sound_position)</code></pre> is called. The function returns the default marker with only one key, offset, equals to the function argument (player_current_sound_position).<br>
</li><li>If function, <b><code>newMarker</code></b> is the function which creates user-defined marker objects by overriding the default <code>player.newMarker</code> described above. The function must receive as argument the marker offset (float) and return a JavaScript object whose only requirements is to have the property offset equals to the function argument, e.g.:<br>
<pre><code>function(offset){<br>
   return {<br>
           offset: parseFloat(offset),<br>
           description: "",<br>
           title: "",<br>
           isEditable: true, <br>
           isSavedOnServer: false<br>
   }<br>
};<br>
</code></pre>
</li></ol></li></ul><blockquote>Obviously, the object returned by <b><code>newMarker</code></b> should be consistent with the elements of the parameter <b><code>markersArray</code></b>, if the latter is provided as a non emtpy array.</blockquote>

<blockquote><font color='#666'>Notes: the marker offset <b>must</b> be a JavaScript number (we provided as hint the use of JavaScript function <code>parseFloat</code> in the example above). <b>It is extremely important for each offset to be a number</b>. As JavaScript is a weakly typed language, passing non-number offsets might lead to subtle errors to catch: imagine for instance two markers with offsets "10.5" and "9.5" (strings). The markers would be normally inserted in the map. However, as "10.5" <code>&lt;</code> "9.5", their insertion order would be incorrect, and the insertion index of any other marker inserted afterwards unpredictable. As a consequence, the positions of the marker labels on the player ruler would mismatch their index, and - even worse - any custom method that relies upon  <a href='#Markers_control_and_management.md'>markers control and management</a> might fail).</blockquote>

<blockquote>The property isEditable, although not mandatory, determines whether or not the marker offset can be changed, i.e. if it can be moved on the player ruler. If missing, it defaults to false. Therefore, in the example above, clicking the button 'add marker' will display a dynamic marker (movable with mouse events); on the other hand, if <b>newMarker</b> is simply set to <code>true</code>, clicking the button 'add marker' will display a static marker (<code>isEditable</code> is missing by default). The editable property of each marker can be changed via the property <code>player.setMarkerEditable</code>, as explained in details in the <a href='#Markers.md'>player marker properties</a></blockquote>

<blockquote>Summarizing, a marker is a JavaScript object which the user must provide at least with one required key, <code>offset</code>, as float. However, to tell the whole story, a marker is stored in the markerMap as an object with at least three properties: <code>offset</code> (float, required), <code>isEditable</code> (boolean, if missing is set to <code>false</code>) and <code>id</code> (if missing is automatically created by the markerMap and must be unique for each marker). By default it is a string with fixed length derived from the current timestamp and a randomly generated number. A user defined <code>id</code> must be unique for each marker and should be consistently comparable against other <code>id</code>s, as for markers with the same offset, <code>id</code>s will determine the necessary sort order and, if equal, that the two markers are equal. <b>In general, there is no reason to implement a custom id</b></font><i></blockquote></i>

<pre><code> onError: function(string)<br>
</code></pre>
<blockquote>a callback to be executed when an error occurs. This includes non existing container, sound duration NaN (or non-positive) etcetera. The string argument passed to the callback is the error message. It is <b>not</b> fired on sound errors (see notes below for <code>onReady</code>)</blockquote>

<pre><code> onReady: function(player)<br>
</code></pre>
<blockquote>a callback to be executed when the player is fully loaded. The argument <code>player</code> passed to the callback is the newly created player, which in any case from the execution of this callback on will be globally accessible via the variable <code>Timeside.player</code>.</blockquote>

<blockquote><font color='#666'>Notes: onReady is fired when the player is fully loaded, although the wave image could still be loading. To know the status of the loading process, use the property <code>player.isImgRefreshing</code> (see <a href='#The_Player_object.md'>player properties and methods</a> for details). To execute a callback once the player is ready and the sound image is fully loaded, use the property <code>onReadyWithImage</code> (see below)</font><i></blockquote></i>

<blockquote><font color='#666'><code>onReady</code> is executed even in case of sound error (e.g. if <code>soundManager</code> or the player sound object is not succesfully initialized) as this does not interfere with the correct player layout. Sound error messages are stored in the property <code>player.soundErrorMsg</code>. Bad sound urls (eg, pointing to non existing files) are cought once the <code>player.play</code> is called, so that at this stage <code>player.soundErrorMsg</code> might be empty (no error) even if the sound is not playable</font><i></blockquote></i>

<pre><code> onReadyWithImage: function(player)<br>
</code></pre>
<blockquote>a callback to be executed when the player is fully loaded <b>and its image has been loaded</b>. This callback is likely to be called after <code>onReady</code>. The argument <code>player</code> passed to the callback is the newly created player, which in any case from the execution of this callback on will be globally accessible via the variable <code>Timeside.player</code></blockquote>

<blockquote><font color='#666'><code>onReadyWithImage</code> is also executed even if the sound object of the player is not succesfully initialized (see notes on <code>onReady</code> above)</font><i></blockquote></i>

<pre><code> messages: Object<br>
</code></pre>
<blockquote>Property setting an object with the default messages to be displayed on the wait panel. The player has three types of default messages:<br>
<pre><code>  messages.loading = "loading"              //displayed when playback is started and sound is loading<br>
  messages.buffering = "buffering"          //displayed when playback is started and sound is buffering<br>
  messages.imgRefreshing = "refreshing img" //displayed when image is being loading and not-yet displayed<br>
</code></pre>
which can be customized in <code>messages</code>. These properties can be also set after the player is loaded via the property <code>player.msgs</code>. Setting a property to the empty string (or any other value which evaluates to false, e.g. undefined) will NOT display the wait panel when the corresponding event is fired</blockquote>


<h3>Markers control and management</h3>
With customized marker objects (i.e., when the parameter <b><code>newMarker</code></b> described above is a user defined function) the user might want also to interact with the player in order to add/edit/remove markers.<br>
As we will see more specifically in the <a href='#Timeside_UI_code.md'>last section</a>, each class defined in the variable TimeSide (as well as the <b>player</b> object) is <a href='http://ejohn.org/blog/simple-javascript-inheritance/'>instance of</a> <code>Timeside.classes.TimesideClass</code>, a function with methods for adding listeners and action notifications, the same way standard event types (e.g., 'onclick') are bound to document elements.<br>
<br>
The marker-specific eventTypes bound to the player object are three (for a complete list, see subsection "Default event types" in <a href='#Event_listening_and_notification.md'>Event listening and notification</a>):<br>
<pre><code>player.bind('markerAdded',callback(data));<br>
player.bind('markerRemoved',callback(data));<br>
player.bind('markerMoved',callback(data));<br>
</code></pre>
where callback is a function which must take a parameter <code>data</code> (JavaScript object), which reads:<br>
<br>
'markerAdded':<br>
<pre><code>data={<br>
  marker: object, //The newly created marker<br>
  index: int      //The index of the newly created marker<br>
}<br>
</code></pre>
'markerRemoved':<br>
<pre><code>data={<br>
  marker: object, //The marker removed<br>
  index: int      //The index of the removed marker<br>
}<br>
</code></pre>
'markerMoved':<br>
<pre><code>data={<br>
  marker: object,   //The marker moved<br>
  oldOffset: float, //The old offset of the marker. The new offset (new offset != old offset) is marker.offset<br>
  fromIndex: int,   //The old index of the moved marker<br>
  toIndex: int,     //The new index of the moved marker. It might be equal to fromIndex <br>
                    // if the marker did not "cross" any other marker in the markermap  <br>
}<br>
</code></pre>
<font color='#666'>If you are familiar with jQuery, note that the syntax is exactly the same as <code>jQuery.bind(eventType,handler)</code>, the only difference is a third (optional) parameter which denotes the reference to the <b>this</b> keyword inside the callback, e.g.:</font><i><pre><code>player.bind('markerAdded',function(data){<br>
  var p = this; //refers to Timeside.player object<br>
},Timeside.player);<br>
</code></pre></i>

<h4>Examples</h4>
As a (quite foolish) example, if we want to alert the user every time a new marker is added, we can write:<br>
<pre><code>Timeside.player.bind('markerAdded', function(data){<br>
  alert('new marker added at time '+data.marker.offset+' and index '+data.index);<br>
});<br>
</code></pre>
and click on the player 'add marker' button to see the alert dialog displaying the message<br>
<br>
As a more complex example, imagine we want a player where:<br>
<ul><li>each marker has a title property which is editable<br>
</li><li>markers can be removed from the player ruler (note that the player by default has no control - e.g., button - to remove markers. Therefore, we can bind whatever callback to the event type 'markerRemoved', but we still miss a control calling <code>player.removeMarker</code>, which will <i>fire</i> the events of type 'markerRemoved')</li></ul>

To achieve this, we can imagine that each time the user presses the 'add marker' button on the player, we add a 'row' on a spearated <code>&lt;div&gt;</code> (which we created) which could look like this:<br>
<br>
<img src='http://files.parisson.com/telemeta/markerdivSchema.png' />

<b>1st step</b>: Initialize the player with newMarkerCallback returning objects of the type, e.g.:<br>
<pre><code>{<br>
  isEditable: true,<br>
  offset: parseFloat(offset), <br>
  title: "", //default marker title when, e.g., the add marker button is pressed<br>
}<br>
</code></pre>

<b>2nd step</b>: add bindings to the player:<br>
<pre><code>var p = Timeside.player;<br>
<br>
p.bind('markerAdded', function(data){<br>
  var m = data.marker; //reference to the newly created marker<br>
  <br>
  //create html elements: <br>
  var okButton = jQuery('&lt;input/&gt;').attr('type','button').val('ok');<br>
  var textInput = jQuery('&lt;input/&gt;').attr('type','text').val(m.title);<br>
  var deleteButton = jQuery('&lt;input/&gt;').attr('type','button').val('delete');<br>
<br>
  //do other stuff, e.g. append elements to a div or a container etcetera...<br>
  <br>
  //Now: When the user clicks the ok button, set marker title according to the text input value<br>
  okButton.click(function(){ <br>
      m.title = textInput.val(); <br>
  });<br>
<br>
  //When the user clicks the remove button, remove the marker<br>
  //this will fire events of type 'markerRemoved'<br>
  deleteButton.click(function(){ <br>
      p.removeMarker(m); //note that p.removeMarker(data.index) is safe ONLY if the markers cannot be moved<br>
  });<br>
});<br>
<br>
//listen for marker removal events:<br>
p.bind('markerRemoved', function(data){<br>
  //remove components, e.g., the &lt;div&gt; containing the input, ok and delete button associated to the removed marker<br>
});<br>
<br>
//listen for marker move events:<br>
p.bind('markerMoved', function(data){<br>
  //reorder inputs and ok buttons to match the marker order<br>
  //Eg:<br>
  //detach div at index data.fromIndex<br>
  //re-insert the div at index data.toIndex<br>
});<br>
</code></pre>

<h2>Layout</h2>
<h3>CSS and skins</h3>

The appearance of TimeSide UI can be fully customized through CSS rules, applied to the<br>
<a href='#Markup_structure.md'>markup structure</a>.<br>
<br>
Two default skins are also provided in the skins/ subfolder. They can be set in the standard way within the <code>&lt;head/&gt;</code> tag:<br>
<br>
<pre><code>&lt;link type="text/css" href="timeside-ui/skin/lab/style.css" /&gt;<br>
</code></pre>
or<br>
<pre><code>&lt;link type="text/css" href="timeside-ui/skin/classic/style.css" /&gt;<br>
</code></pre>

The default skins exploit contextual selectors (e.g., ".player .ts-ruler"), so the player <b>must</b> embedded in (or in a child of) a div of class 'ts-player', e.g.:<br>
<br>
<pre><code>    &lt;div class="ts-player" /&gt;<br>
       &lt;!--player is contained here somewhere...--&gt;  <br>
    &lt;/div&gt;<br>
</code></pre>

If you don't like this restriction, feel free to modify the css according to your needs. We only suggest to embed the player this way at first to see what's going on behind the scene (by exploring the css files) before providing your custom skins.<br>
<br>
<br>
<font color='#666'><i>Notes (in the remainder of this section, we will denote R, W and C as player ruler, wave and control <code>&lt;div&gt;</code>s, whose css class selectors are ".ts-ruler", ".ts-wave" and ".ts-control", respectively. See player figure and and <a href='#Markup_structure.md'>markup structure</a> in the <a href='#Introduction.md'>Introduction</a>):</i>

<ul><li><i>Css skins should customize player <b>appearence</b>. Some css properties might break the player layout, resulting in some components not properly positioned or hidden. Assuming this is not what you are aiming to, properties such as "position", "display", "float" and "overflow" should not be specified on any of the player elements, unless you really know what you are doing. In any case, consider that some styles properties will be always set (and thus overridden, if any) inside the JavaScript code (e.g., R, W and C will have all 'position' = 'relative' and 'overflow' = 'hidden')</i></li></ul>

<ul><li><i>Player dimensions (css width and height properties) can be specified through css. As a rule of thumb keep in mind that no width ('auto') on a <code>&lt;div&gt;</code> means that the total width of the <code>&lt;div&gt;</code> is automatically computed to fit the parent, and no height ('auto') on a <code>&lt;div&gt;</code> means that the total height of the <code>&lt;div&gt;</code> is automatically computed to fit its content.</li></ul></i>

<blockquote>Therefore, setting player total width is quite straighforward: you can set it by means of css width property on W (this is actually what happens when <b>imgSize</b> width is specified), or you can simply provide no css width property at all for any player <code>&lt;div&gt;</code>, letting the player fit the avilable parent width. In any case, according to what stated above, do not specify the same width property for W, R and C (is useless), and do not specify different width propertis for W, R and C (is dangerous). <a href='Hidden comment: Note that setting width="100%" will force the content alone to be 100%, meaning the padding etc. will stick out of the div, making it larger than the parent'></a></blockquote>

<blockquote>Setting the player total height is done separately on W, R and C css height properties in the standard way, i.e., by means of css rules applied on them or their contained elements. Two remarks on JavaScript code: first, most of W sub components (sound image, marker and ruler vertical lines) are "stretched" automatically to fit all the available room (which also means that some of their css can not be customized), so W <b>must</b> have a nonzero non 'auto' height. Second, the height of the vector-graphics ruler of R is set as the height of two lines of text, i.e., according to R 'font-size' and 'line-height' css properties (if missing they wil be inherited from the parent)<i></blockquote></i>

<ul><li><i>Classes relative to vector graphics elements (beginning with '.ts-svg-') have specific <a href='http://www.w3.org/TR/SVG/styling.html'>svg css syntax</a>. As already mentioned, svg is not supported in all browsers, and the TimeSide library delegates Raphael for building vml graphics (an old format of IE), in case. Raphael has a lot of attributes which can be set on the graphics, whatever format they are. In order to customize entirely and cross browser the player through css, when svg is not supported the TimeSide library parses stylesheet classes and converts its rules into suitable Raphael attributes. However, note that:<br>
<ul><li>Many but not all css properties are supported for conversion. Actually, only those that have a corresponding attribute translation in Raphael. Supported css properties are:</i>
<pre><code>     "clip-rect", "cursor",'fill', "fill-opacity", "opacity", <br>
     "stroke", "stroke-dasharray", "stroke-linecap", "stroke-linejoin",<br>
     "stroke-miterlimit","stroke-opacity","stroke-width", "text-anchor"<br>
</code></pre>
</li><li><i>The TimeSide parser <b>recognizes only stand-alone class selectors</b>, without spaces or commas (it is not the purpose of the library to have full class parsing capabilities, even more so when the matter is an old and not standard graphics format). In other words</i>
<pre><code>    .ts-svg-marker-canvas{<br>
       stroke-width:2;<br>
    }<br>
</code></pre>
</li></ul><blockquote><i>will set a stroke of width 2 on the elements of class 'ts-svg-marker-canvas' in all browsers, whereas</i>
<pre><code>    #player .ts-svg-marker-canvas{ <br>
       stroke-width:2;<br>
    }<br>
</code></pre>
<i>will <b>not</b> set the desired stroke width on, e.g., IE 7-8<br>
</blockquote><ul><li>Apparently, Raphael has a bug on color properties specified as predefined/Cross-browser color names (e.g.: 'white', 'yellow'). Thus this would break in IE7-8:</i>
<pre><code>    .ts-svg-ruler-lines{<br>
       stroke: white; //ERROR on non svg supporting browsers which PREVENTS the player to be loaded!!<br>
    }<br>
</code></pre>
</li></ul><blockquote><i>Any other value seems to be safe. We suggest however to provide those properties as standard hexadecimal values:</i>
<pre><code>    .ts-svg-ruler-lines{<br>
       stroke: #ADADAD;<br>
    }<br>
</code></pre>
</blockquote></li><li><i>Just keep in mind that the default skins implement contextual selectors (e.g., ".player .ts-ruler") for two main reasons: avoid css "collisions" with potential elements of the page with the same class name (e.g., <code>.ts-ruler</code>) and allow dynamically skinnable players, e.g. by changing the class attribute of the outer container. As we have seen, this is unfortunately not (yet) possible for backward compatibility with IE7-8. In any case, if you are really interested to dynamically skinnable players, you can achieve the goal for the moment by simply creating your own css and dynamically adding/removing them to the <code>&lt;head/&gt;</code> tag of the page</i></font></li></ul>

<h3>Dynamic resizing</h3>

Unlike Flash-based media players, the DHTML-based TimeSide player can be resized<br>
in various ways (as explained in the previous section) by dynamically modifying the CSS rules of the player elements or those of one of its containers in the HTML page, or by simply resizing the browser window if the player size is relative to the window.<br>
<br>
The <code>TimeSide.Player</code> class can automatically track browser window resize events if its property <code>setDynamicsResize</code> is called with <code>true</code> as argument (it is false by default). In this case, the player checks at regular intervals (JavaScript <code>setInterval</code> method) potential size changes. If it is the case, it calls<br>
<pre><code>player.refreshImage()<br>
</code></pre>
which in turn calls <code>player.imageCallback</code> (which can specified when loading the player via the parameter <b><code>soundImage</code></b>). Obviously, for accurate high quality<br>
server-side resizing/resampling, <code>setDynamicResize(true)</code> should be called if <code>player.imageCallback</code> is a callback returning a width- and height-dependent image (where width and height are the callback arguments).<br>
<br>
<font color='#666'>Note that in case of repeated size changes (such as, i.e., window mouse resizing while dragging) only the last resize is fired. This attempts to prevent several unnecessary <code>refreshImage</code> calls which  might lead to an unresponsive page. Basically, each time a player size change is detected, <code>refreshImage</code> is called within a delay of time only if meanwhile it's size has not changed again</font>

<a href='Hidden comment: 
The method is (or at least, should be) smart enough  However, it can"t
reliably detect size changes that originate from the DOM content. In that kind of circumstance, it is
recommended to call TimeSide.Player.resize() to ensure that the UI is properly redrawn.

For example, using jQuery:
<pre><code>$("#myplayer").width(500);
player.resize() // player is a TimeSide.Player object
</code></pre>

Additionally, for accurate waveforms and/or spectrograms,  the graph can be dynamically loaded
by passing a callback to the !TimeSide.Player constructor. This callback is called
whenever the image width and/or height change, and allows to perform high quality
server-side resizing/resampling.

<pre><code>function get_image(width, height) {
    // Return the dynamic image src:
    return "generate_graph?w=" + width + "&h=" + height;
}

TimeSide.load(function() {
    var player = new TimeSide.Player("#myplayer", { image: get_image });
});
</code></pre>
'></a><br>
<h2>Timeside UI code</h2>
The TimeSide player is created and can be manipulated using a JavaScript <a href='http://ejohn.org/blog/simple-javascript-inheritance/'>object oriented</a>  API. The JavaScript inheritance-simulating techniques is accomplshed by means of a 'Class' function which is the ancestor class of all TimeSide classes:<br>
<br>
<h3>Inhertance Structure</h3>
<pre><code>/*<br>
 *Function name      defined in:        Description <br>
 */<br>
  Class               (`timeside.js`)    //The base javscript function with class functionalities: <br>
  |                                      // simple inheritance and super method calling<br>
  | <br>
  +- TimesideClass    (`timeside.js`)    //Class implementation ancestor class of all Timeside classes<br>
     |<br>
     +- RulerMarker   (`rulermarker.js`) //TimesideClass for building each marker on the ruler (including pointer)<br>
     |<br>
     +- Player        (`player.js`)      //TimesideClass for building the player<br>
     |<br>
     +- TimesideArray (`timeside.js`)    //TimesideClass with array-like properties and methods<br>
        |<br>
        +- MarkerMap  (`markermap.js`)   //TimesideArray for managing markers<br>
        |<br>
        +- Ruler      (`ruler.js`)       //TimesideArray for building the ruler and managing rulermarkers<br>
</code></pre>

As already mentioned, the only variable created on the window object is the <code>Timeside</code> variable, which includes:<br>
<pre><code>Timeside = {<br>
    Class,             //The Class object whereby each element of Timeside.classes has been created,<br>
    classes : {<br>
        TimesideClass, //accessible with Timeside.classes.TimesideClass <br>
        TimesideArray, //accessible with Timeside.classes.TimesideArray<br>
        MarkerMap,     //...<br>
        Ruler,         //...<br>
        RulerMarker,   //... <br>
        Player         //...<br>
    },<br>
    player, //The player object = new Timeside.classes.Player(...) accessible with Timeside.player<br>
            //when the player is created:  <br>
            //player.getMarkerMap() returns the player markerMap object = new Timeside.classes.MarkerMap(...)<br>
            //player.getRuler() returns the player ruler object = new Timeside.classes.Ruler(...)<br>
            //player.getRuler().toArray()[i] returns the ruler i-th marker = new Timeside.classes.RulerMarker(...)<br>
            //player.getRuler().getPointer() returns the ruler pointer = new Timeside.classes.RulerMarker(...) as well<br>
    load(), //Function to be called in order to initialize Timeside.player (see above)<br>
    config, //object with configuration properties to be used in load<br>
    utils   //object with utilities functions/properties to be used by Timeside classes<br>
}<br>
</code></pre>

Therefore, once fully initialized, the user can work with the accessible <code>Timeside.player</code> object (instance of <code>Timeside.classes.Player</code>)<br>
<br>
<h3>The Player object: properties and methods</h3>
Here properties and method of the player object. <code>player</code> is a shorthand for <code>Timeside.player</code>

<h4>Playback</h4>

<pre><code>player.play()<br>
</code></pre>
<blockquote>Starts playback. This method is called by the 'play' button on the control <code>&lt;div/&gt;</code></blockquote>

<pre><code>player.setSoundPosition(offset)<br>
</code></pre>
<blockquote>Sets the sound position and moves the pointer on the player ruler accordingly. This method is called by the 'play' button on the control <code>&lt;div/&gt;</code>
</blockquote><ul><li>offset (<code>float</code>): the offset of the new sound position in the format seconds.milliseconds (e.g., <code>45.562</code>)</li></ul>

<pre><code>player.playState //Read-only property. Do not modify!<br>
</code></pre>
<blockquote>Property returning an integer indicating the player play state. <i>Read-only property. Do not modify!</i>
Possible values are:<br>
<ul><li>0: player not playing<br>
</li><li>1: player playback started: sound loading<br>
</li><li>2: player playback started: sound buffering<br>
</li><li>3: player playback started, nor buffering neither loading. This condition is most likely corresponding to the "sound heard" condition</li></ul></blockquote>

<pre><code>player.pause()<br>
</code></pre>
<blockquote>Pauses playback. This method is called by the 'pause' button on the control <code>&lt;div/&gt;</code> (this method is actually stopping the sound object. This allows to more reliably work with the sound.position property)</blockquote>

<pre><code>player.rewind()<br>
</code></pre>
<blockquote>Sets the sound position (and moves the pointer) to the previous marker position (according to the current sound position), or to the start of sound if no previous marker is found. This method is called by the 'rewind' button on the control <code>&lt;div/&gt;</code></blockquote>

<pre><code>player.forward()<br>
</code></pre>
<blockquote>Sets the sound position (and moves the pointer) to the next marker position (according to the current sound position), or to the end of sound if no previous marker is found. This method is called by the 'forward' button on the control <code>&lt;div/&gt;</code></blockquote>

<pre><code>player.getSound()<br>
</code></pre>
<blockquote>Returns the <a href='http://www.schillmania.com/projects/soundmanager2/doc/'>sound object</a> associated to the player. Manipulating the sound object directly is discouraged, as it might interfere with the player object. This method is intended for retrieving properties not directly accessible via the player object. Returns <code>undefined</code> if a sound error occurs</blockquote>

<pre><code>player.soundErrorMsg<br>
</code></pre>
<blockquote>Returns the empty string if the <a href='http://www.schillmania.com/projects/soundmanager2/doc/'>sound object</a> of the player has been succesfully initialized. Otherwise, it is a string denoting the error occurred. This includes soundManager errors (including flash errors for non-html5 supporting browsers), bad sound-object (or sound-object parameters), invalid urls. The case of urls not pointing to existing and "playable" audio files will be cought only the first time <code>player.play</code> is called.</blockquote>

<pre><code>player.showSoundErrorMessage()<br>
</code></pre>
<blockquote>Callback to be executed when <code>player.play</code> is called and the <a href='http://www.schillmania.com/projects/soundmanager2/doc/'>sound object</a> of the player has not been succesfully initialized. It can be overridden: by default, it shows an alert dialog with the content of <code>player.soundErrorMsg</code></blockquote>

<pre><code>player.soundPosition //Read-only property. Do not modify!<br>
</code></pre>
<blockquote>Returns the current sound position, in the format seconds.milliseconds (e.g., <code>45.672</code>). <i>Read-only property. Do not modify!</i></blockquote>

<pre><code>player.getSoundDuration()<br>
</code></pre>
<blockquote>Returns the total duration of the sound, in the format seconds.milliseconds (e.g., <code>45.672</code>)</blockquote>

<pre><code>player.setSoundVolume(volume)<br>
</code></pre>
<blockquote>Sets the volume of the sound. This method is called by the volume-related button(s) on the control <code>&lt;div/&gt;</code>
</blockquote><ul><li>volume (<code>int</code>): an integer between zero and 100</li></ul>

<pre><code>player.soundVolume //Read-only property. Do not modify!<br>
</code></pre>
<blockquote>Returns a number between 0 and 100 denoting the sound volume. <i>Read-only property. Do not modify!</i></blockquote>

<pre><code>player.readyState()<br>
</code></pre>
<blockquote>Returns a numeric value indicating a sound's current load status:<br>
</blockquote><ul><li>0 = uninitialised<br>
</li><li>1 = loading<br>
</li><li>2 = failed/error<br>
</li><li>3 = loaded/success<br>
<font color='#666'>Note: If the player is created by passing an already created sound object, <code>readyState()</code> might be 2 even if <code>player.soundErrorMsg</code> is empty. Otherwise, if the player is created by means of a url string or an object denoting the sound object default properties, <code>player.soundErrorMsg</code> might be a non-empty string even if <code>readyState()</code> is not 2 (e.g., it might be 0, i.e.  uninitialized)</font><i><h4>Markers</h4></li></ul></i>

<pre><code>player.newMarker(offset)<br>
</code></pre>
<blockquote>Function that builds and returns the marker object with offset property equals to <code>offset</code>. Can be overridden (see above) for custom markers<br>
</blockquote><ul><li>offset (<code>float</code>): the offset of the marker to be created in the format seconds.milliseconds (e.g., <code>45.562</code>)</li></ul>

<pre><code>player.addMarker(offset)<br>
</code></pre>
<blockquote>Adds a new marker at offset . Calls by default <code>player.newMarker(offset)</code> and puts in the map the returned marker. This method is called by the 'add marker' button on the control <code>&lt;div/&gt;</code> (if visible)<br>
</blockquote><ul><li>offset (<code>float</code>): the offset of the marker to be created in the format seconds.milliseconds (e.g., <code>45.562</code>)</li></ul>

<pre><code>player.removeMarker(identifier)<br>
</code></pre>
<blockquote>Removes a marker<br>
</blockquote><ul><li>identifier (<code>int</code> or <code>object</code>): if number, it indicates the index of the marker to be removed. Otherwise, it must be a valid marker belonging to the marker map</li></ul>

<pre><code>player.moveMarker(identifier, newOffset)<br>
</code></pre>
<blockquote>Moves a marker to a new offset<br>
</blockquote><ul><li>identifier (<code>int</code> or <code>object</code>): if number, it indicates the index of the marker to be removed. Otherwise, it must be a valid marker belonging to the marker map<br>
</li><li>newOffset (<code>float</code>): the new marker offset in the format seconds.milliseconds (e.g., <code>45.562</code>)</li></ul>

<pre><code>player.getMarker(index)<br>
</code></pre>
<blockquote>Returns the index-th marker of the player, or undefined if index is lower than zero or greater than <code>len - 1</code>, where <code>len</code> is the number of markers of the player<br>
</blockquote><ul><li>index (<code>int</code>): the marker index</li></ul>

<pre><code>player.setMarkerEditable(identifier, value)<br>
</code></pre>
<blockquote>Sets a marker property <code>isEditable</code> = <code>value</code>. You can change also directly the property <code>isEditable</code> on each markerm but this will not fire events of type "markerEditStateChanged", so avoid it if you want notifications when a marker has changed its editable state  (see "Default event types" in the section <a href='#Event_listening_and_notification.md'>Event listening and notification</a>)<br>
</blockquote><ul><li>identifier (<code>int</code> or <code>object</code>): if number, it indicates the index of the marker to be removed. Otherwise, it must be a valid marker belonging to the marker map<br>
</li><li>value (<code>boolean</code>): the value of the property isEditable to be set</li></ul>

<pre><code>player.each(callback)<br>
</code></pre>
<pre><code>player.each(startIndex, callback)<br>
</code></pre>
<pre><code>player.each(startIndex, endIndex, callback)<br>
</code></pre>
<blockquote>Iterates over the player markers. Each time <code>callback</code> runs, it is passed two arguments: the current loop iteration <i>i</i>, and the marker at index <i>i</i>.<br>
</blockquote><ul><li>startIndex (<code>int</code>) <b>optional</b>: the start index, <i>inclusive</i> (if missing, it defaults to 0)<br>
</li><li>endIndex (<code>int</code>) <b>optional</b>: the end index, <i>exclusive</i>. If missing, it defaults to the number of player markers<br>
</li><li>callback (<code>function</code>): a function accepting two arguments, the current marker index and the current marker.<br>
</li></ul><blockquote>Example: print on the console the informations about <i>all</i> the current markers:<br>
<pre><code>  player.each(<br>
      function(i,m){<br>
         console.log('marker # ' + i + ' at time: ' + m.offset);<br>
      }<br>
  );<br>
</code></pre></blockquote>

<h4>Layout</h4>

<pre><code>player.imageCallback(width, height)<br>
</code></pre>
<blockquote>Function that returns the wave image to be displayed according to the wave <code>&lt;div/&gt;</code> width and height. The function must return a valid URL pointing to an image. This allows, e.g., to perform high quality server-side resizing/resampling by querying Timeside grapher for a sound image with given width and height. This callback is specified as starting player parameter (see above)<br>
</blockquote><ul><li>width (<code>number</code>) the new image width<br>
</li><li>height (<code>number</code>) the new image height</li></ul>

<pre><code>player.refreshImage()<br>
</code></pre>
<blockquote>Forces a refresh of the image. Set the wave image <code>src</code> to the url returned by <code>imageCallback</code></blockquote>

<pre><code>player.isImgRefreshing //Read-only property, do not modify!<br>
</code></pre>
<blockquote>Boolean value indicating whether or not the wave image is being loading and not-yet displayed. <i>Read-only property. Do not modify!</i></blockquote>

<pre><code>player.resize()<br>
</code></pre>
<blockquote>Forces a resize of the player. It resizes the player ruler and control and calls <code>player.refreshImage()</code></blockquote>

<pre><code>player.setDynamicResize(value)<br>
</code></pre>
<blockquote>Sets dynamic resize. If <code>value</code> is true, the player starts checking at regular interval potential size changes and in case, it will set the wave image <code>src</code> to the url returned by <code>imageCallback</code>
</blockquote><ul><li>value (<code>boolean</code>): if true, the player checks for size changes at regular interval (JavaScript <code>setInterval</code> method). If false, the player stops checking (JavaScript <code>clearInterval</code> method) and player size changes do not call any image refresh (false is the default)</li></ul>

<pre><code>player.getImageUrl()<br>
</code></pre>
<blockquote>Returns a string of the URL of the wave image (i.e., the <code>src</code> attribute of the wave <code>&lt;img/&gt;</code>)</blockquote>

<pre><code>player.getImageSize()<br>
</code></pre>
<blockquote>Returns an object with two number properties, width an height, denoting the size of the wave image</blockquote>


<h4>Miscellaneous</h4>

<pre><code>player.setWait(message)<br>
</code></pre>
<blockquote>Sets the content of the wait panel (<code>&lt;div/&gt;</code>) in the lower right corner of the player (see player image in the <a href='#Introduction.md'>Introduction</a>) and hides or shows the <code>&lt;div/&gt;</code> accordingly<br>
</blockquote><ul><li>message (<code>string</code>): If it evaluates to false (e.g., undefined, empty string) it hides the <code>&lt;div/&gt;</code>. Otherwise shows it and sets its html content to <code>message</code></li></ul>

<pre><code>player.msgs<br>
</code></pre>
<blockquote>Property returning an object with the default messages to be displayed on the wait panel (<code>&lt;div/&gt; innerHTML</code>). There are currently three types of default messages:</blockquote>

<pre><code>  msgs.loading = 'loading'              //displayed when playback is started and sound is loading<br>
  msgs.buffering = 'buffering'          //displayed when playback is started and sound is buffering<br>
  msgs.imgRefreshing = 'refreshing img' //displayed when image is being loading and not-yet displayed<br>
</code></pre>

<blockquote>These properties can be customized after the player is loaded. Setting a property of <code>player.msgs</code> to the empty string (or any other value which evaluates to false, e.g. undefined) will NOT display the wait panel when the corresponding event is fired</blockquote>

<h4>Event listening and notification</h4>
<pre><code>player.bind(eventType, callback) <br>
</code></pre>
<pre><code>player.bind(eventType, callback, thisArgInCalback) <br>
</code></pre>
<blockquote>Binds a callback to eventType. The function callback will be executed each time <code>fire(eventType)</code> will be called on the player (see below).<br>
</blockquote><ul><li>eventType (<code>string</code>) the event type name<br>
</li><li>callback (<code>function</code>) the function to be executed. It <i>always</i> takes as argument a JavaScript object <code>data</code> which is populated by properties when the eventType is fired.<br>
</li><li>thisArgInCalback (<code>object</code>) <b>optional</b>: specifies the optional <code>this</code> keyword in <code>callback</code></li></ul>

<pre><code>player.fire(eventType)<br>
</code></pre>
<pre><code>player.fire(eventType, data)<br>
</code></pre>
<blockquote>Fires (triggers) all callbacks associated to eventType by means of <code>player.bind(eventType,...)</code>. It does nothing if no callback is bound to <code>eventType</code>
</blockquote><ul><li>eventType (<code>string</code>) the event type name<br>
</li><li>data (<code>object</code>) <b>optional</b>: A JavaScript object which is populated by properties to be passed as argument to all callbacks registered to eventType by means of <code>player.bind(eventType,...)</code> (see above). If missing it defaults to the empty JavaScript object <code>{}</code></li></ul>

<pre><code>player.unbind()<br>
</code></pre>
<pre><code>player.unbind(eventType)<br>
</code></pre>
<blockquote>Unbinds (i.e., removes from memory) all callbacks bound to eventType<br>
</blockquote><ul><li>eventType (<code>string</code>) <b>optional</b>: the eventType name. If missing or undefined, it removes <b>all</b> custon (not default) bindings for <b>all</b> eventTypes</li></ul>

As in <a href='http://api.jquery.com/bind/'>jQuery bind</a>, If the eventType string contains a period (.) character, then the event is namespaced. The period character separates the event from its namespace. For example, in the call <code>.bind('markerMove.name', function(data){...})</code>, the string "markerMove" is the event type, and the string "name" is the namespace. Namespacing allows us to unbind or trigger some events of a type without affecting others. Accordingly, when a callback is bound in this fashion, we can still unbind it the normal way:<br>
<code>.unbind('markerMove')</code> or alternatively, if we want to avoid affecting other callbacks, we can be more specific, i.e.  <code>.unbind('markerMove.name')</code>. Note that TimeSide namespacing does not have the whole funtionalities of   <a href='http://api.jquery.com/bind/'>jQuery namespacing</a>, please refer only to those just described. Moreover, consider that in the TimeSide library a period character is considered a namespace separator only if it splits non-empty strings. In other words, event types such as ".name" or "name." will be considered as they are, without namespaces. As in jQuery namespacing, if a string contains more than a period character, the first period only will be considered the namespace separator.<br>
<br>
<a href='Hidden comment: 
_<font color=#666>Note: event notification is optimized for speed of the method, not for memory usage. That means, with namespacing the same function is stored more than once in the internal map storing listeners. This allows a call to fire to be faster, the drawback being more memory used

Unknown end tag for </font>

_
'></a><br>
<br>
<h5>Default event types</h5>
Functions which interact with the player can bind calbacks to the following event types implemented by default:<br>
<br>
<table width='55%' border='1'>
<tr>
<blockquote><td valign='top'>Event type</td>
<td width='25%' valign='top'>Fired when:</td>
<td valign='top'>Passed <code>data</code> argument:</td>
</tr>
<tr>
<td valign='top'>"markerCrossed"</td>
<td width='25%' valign='top'>a marker has been crossed while playing</td>
<td valign='top'>
<pre><code>{<br>
 index: int,                   //the index of the marker being crossed<br>
 marker: object,               //the marker being crossed<br>
 currentSoundPosition: float,  //self explanatory<br>
 nextMarkerTimeInterval: array //undefined if the marker being crossed is the last in the <br>
                               //marker map. Otherwise, it is an array of two elements defining <br>
                               //the time interval around the next marker offset. <br>
                               //Due to the way event notification is handled in soundManager <br>
                               //while playing, TimeSide detects marker cross events <br>
                               //as soon as the sound position "falls" in an interval <br>
                               //(with predefined time margins) around a marker offset. <br>
                               //This means, e.g., that data.currentSoundPosition might be lower<br>
                               //than marker.offset. The property nextMarkerTimeInterval is useful  <br>
                               //to know, e.g., the minimum time before the next marker cross <br>
                               //event will be fired, e.g.:<br>
                               //data.currentSoundPosition-nextMarkerTimeInterval[0]<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"playStateChanged"</td>
<td width='25%' valign='top'>sound play state has changed.</td>
<td valign='top'>
<pre><code>{<br>
 player: object,        //the player object<br>
 oldPlayState: int,     //self-explanatory. The current play state is player.playState<br>
 endOfPlayback: boolean //true if the play state has changed from 3 to 0 <br>
                        //as a result of the end of sound reached.<br>
                        //This property is useful to distinguish between  <br>
                        //"end of playback" and "pause click" events <br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"markerAdded"</td>
<td width='25%' valign='top'>a marker has been added to the marker map</td>
<td valign='top'>
<pre><code>{<br>
 marker: object, //the newly created marker<br>
 index: int      //the index of the newly created marker<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"markerMoved"</td>
<td width='25%' valign='top'>a marker has been moved in the marker map</td>
<td valign='top'>
<pre><code>{<br>
 marker: object,    //The marker moved<br>
 oldOffset: float,  //the old offset of the marker. <br>
                    //The new offset (new offset != old offset) is marker.offset<br>
 fromIndex: int,    //the old index of the moved marker<br>
 toIndex: int,      //the new index of marker. It might be equal to fromIndex <br>
                    //if the marker did not "cross" any other marker<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"markerRemoved"</td>
<td width='25%' valign='top'>a marker has been removed from the marker map</td>
<td valign='top'>
<pre><code>{<br>
 marker: object, //The marker removed<br>
 index: int      //The index of the removed marker<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"soundPositionSet"</td>
<td width='25%' valign='top'>the method setSoundPosition is called and the pointer has been set. <b>It is not fired while playing</b></td>
<td valign='top'>
<pre><code>{<br>
 player: object,          //The player object<br>
 oldSoundPosition: float  //The old sound position. <br>
                          //it might be equal to player.soundPosition<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"markerEditStateChanged"</td>
<td width='25%' valign='top'>the property isEditable of a marker has been changed via <code>player.setMarkerEditable</code></td>
<td valign='top'>
<pre><code>{<br>
 marker: object,    //The event target marker<br>
 oldValue: boolean, //the old value of the property marker.isEditable<br>
 value: int,        //the new value of the property marker.isEditable<br>
 index: int         //The event target marker index<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"markerMouseEvent"</td>
<td width='25%' valign='top'>a mouse event has been performed on a marker <b>or the pointer</b> on the player ruler</td>
<td valign='top'>
<pre><code>{<br>
 eventName: string, //One of the following (jQuery syntax): <br>
                      "mouseenter", "mouseleave", "mousedown", "dragstart" ,"dragend", "click"  <br>
 eventObj: object,  //The jQuery event object related to the mouse event. Fore details, see<br>
                    //http://api.jquery.com/category/events/event-object/<br>
 index: int,        //The marker index &gt;=0, or -1 if the target of the mouse event is the pointer<br>
 marker: object     //The marker object associated to the mouse event, <br>
                    //or undefined if the mouse event target is the pointer<br>
}<br>
</code></pre>
</td>
</tr>
<tr>
<td valign='top'>"waitShown"</td>
<td width='25%' valign='top'>the wait panel has been shown</td>
<td valign='top'>
<pre><code>{} //empty object<br>
</code></pre>
</td>
</tr>
<tr>
<td width='15%' valign='top'>"waitHidden"</td>
<td width='25%' valign='top'>the wait panel has ben hidden</td>
<td width='50%' valign='top'>
<pre><code>{} //empty object<br>
</code></pre>
</td>
</tr>
<tr>
<td width='15%' valign='top'>"imgRefreshing"</td>
<td width='25%' valign='top'>a new wave image is being loading</td>
<td width='50%' valign='top'>
<pre><code>{} //empty object<br>
</code></pre>
</td>
</tr>
<tr>
<td width='15%' valign='top'>"imgRefreshed"</td>
<td width='25%' valign='top'>the new wave image has been loaded</td>
<td width='50%' valign='top'>
<pre><code>{} //empty object<br>
</code></pre>
</td>
</tr>
</table></blockquote>

<font color='#666'><i>Notes:</i>

<i>Events of type "markerMouseEvent" are fired on markers regardless of the property <code>isEditable</code>, which on the other hand dictates if mouse events move a marker on the player ruler and consequently, if the eventType "markerMoved" is fired.<br>
Due to browser differences in handling mouse events and the need to avoid multiple notifications for different events (e.g., 'click' and 'dragend'), "click", "dragstart" and "dragend" eventNames are fired according to the "mousedown" eventName following the schema:</i>

<i>mouse is pressed: fire "markerMouseEvent" with eventName="mousemove". If the mouse button is the left one, then:<br>
<ul><li>if the mouse is moved: fire (only the first time) "markerMouseEvent" with <code>eventName</code>="dragstart" (<code>eventObj</code> thus refers to a "mousemove" jQuery event)<br>
</li><li>if the mouse is released:<br>
<ul><li>if the mouse was moved: fire "markerMouseEvent" with <code>eventName</code>="dragend"<br>
</li><li>otherwise: fire "markerMouseEvent" with <code>eventName</code>="click"<br>
</li></ul></li></ul><blockquote>thus in both cases, when mouse is released, <code>eventObj</code> refers to a "mouseup" jQuery event</i>
</font>