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

		editable: true,
		allDaySlot: false,

		eventRender: function( event, element ) {
			var start_date = new Date(event.start);
			var end_date = new Date(event.end);

			var start_hour = start_date.getHours();
			var start_minute = start_date.getMinutes();

			var end_hour = end_date.getHours();
			var end_minute = end_date.getMinutes();

			var event_type = "Type: " + event.type
			var event_time = "Time: " + start_hour + ":" + start_minute + " to "  + end_hour + ":" + end_minute
			var event_loc = "Location: " + event.location

			// Check if event is all day and change time if true
			if(event.allDay) {
				event_time = "All-day event";
			}

			// console.log(event);

			// Make a qtip on the element
			element.qtip({ 
			    content: {
			        text: event_type + "<br>" + event_time + "<br>" + event_loc + 
			        '<br><br> <button data-toggle="modal" data-target="#editModuleModal" type="button" class="btn btn-default btn-xs">Edit</button> <form role="form" method="post" action="/removeevent"><input type="hidden" name="event_id" value="' + event.id+ '"><button type="submit" class="btn btn-danger btn-xs">Delete</button></form>',
			        title: event.title
			    },
			    style: {
			        classes: 'qtip-dark qtip-rounded qtip-shadow'
			    },
			    show: {
		            solo: true
		        },
			    hide: {
	                fixed: true,
	                delay: 300
	            },
			});
		},

		eventDrop: function(event, delta, revertFunc) {
	        // alert(event.title + " was dropped on " + event.start.format());

	        // if (!confirm("Are you sure about this change?")) {
	        //     revertFunc();
	        // } else {

	        	var link = "/dragevent?event_id=" + event.id;

	        	link = link + "&all_day=" + event.allDay + "&start=" + event.start + "&end=" + event.end;

	        	console.log(link);
	        	window.location.replace(link);
	        // }
    	}
    })
});