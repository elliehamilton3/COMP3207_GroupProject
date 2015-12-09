// Full Calendar initialize
$(document).ready(function() {

    // page is now ready, initialize the calendar...

    $('#calendar').fullCalendar({
       
        header: {
	        left:   'title',
		    center: 'agendaDay,agendaWeek,month',
		    right:  'today prev,next'
		},

		events: {
		 	url: '/feed',
		},

		// eventAfterRender: function(event, element, view){
		// 	$(this).click();
		// },

		eventRender: function( event, element ) {
			var start_date = new Date(event.start);
			var end_date = new Date(event.end);

			var start_hour = start_date.getHours();
			var start_minute = start_date.getMinutes();

			var end_hour = end_date.getHours();
			var end_minute = end_date.getMinutes();

			element.qtip({ // Grab some elements to apply the tooltip to
			    content: {
			        text: "Type: " + event.type
			        + '<br> Time: ' + start_hour + ":" + start_minute
			        + " to "  + end_hour + ":" + end_minute + " <br>Location: " + event.location,
			        title: event.title
			    },
			    style: {
			        classes: 'qtip-dark qtip-rounded qtip-shadow'
			    },
			    hide: {
	                fixed: true,
	                delay: 300
	            },
			});
		}
    })
});

$(document).ready(function() {
	// $('.fc-content').click();
	// alert("clicked");
});

