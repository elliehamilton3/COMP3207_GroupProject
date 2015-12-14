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
			        '<br><br> <button onclick="createEditModal('+event.id+')" type="button" class="btn btn-default btn-xs">Edit</button> <form role="form" method="post" action="/removeevent"><input type="hidden" name="event_id" value="' + event.id+ '"><button type="submit" class="btn btn-danger btn-xs">Delete</button></form>',
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
function createEditModal(eventid) {        
	console.log(eventid);
	$.getJSON( "/getevent?eventid="+eventid, function( data ) {
		$.each( data, function(key, val) {
			console.log(val);
			$('#editeventname').val(val['name']);
			$('#editeventtype').val(val['event_type']);
			$('#editeventlocation').val(val['location']);
			var startDate = val['start_time'].split("T")[0];
			var startTime = val['start_time'].split("T")[1];

			var endDate = val['end_time'].split("T")[0];
			var endTime = val['end_time'].split("T")[1];
			console.log(startDate);
			var newdate = new Date();

			$("#editstartdate").val(startDate);
			$('#editstarttime').attr('placeholder', startTime);

			$('#editenddate').attr("placeholder", endDate);
			$('#editendtime').val(endTime);
			
			$("#editeventcolor").spectrum({
				color: val['color'],
				showInput: true,
			    className: "full-spectrum",
			    showInitial: true,
			    showPalette: true,
			    showSelectionPalette: true,
			    maxSelectionSize: 10,
			    preferredFormat: "hex",
			    localStorageKey: "spectrum.demo",
			    move: function (color) {
			        
			    },
			    show: function () {
			    
			    },
			    beforeShow: function () {
			    
			    },
			    hide: function () {
			    
			    },
			    change: function() {
			        
			    },
			    palette: [
			        ["rgb(0, 0, 0)", "rgb(67, 67, 67)", "rgb(102, 102, 102)",
			        "rgb(204, 204, 204)", "rgb(217, 217, 217)","rgb(255, 255, 255)"],
			        ["rgb(152, 0, 0)", "rgb(255, 0, 0)", "rgb(255, 153, 0)", "rgb(255, 255, 0)", "rgb(0, 255, 0)",
			        "rgb(0, 255, 255)", "rgb(74, 134, 232)", "rgb(0, 0, 255)", "rgb(153, 0, 255)", "rgb(255, 0, 255)"], 
			        ["rgb(230, 184, 175)", "rgb(244, 204, 204)", "rgb(252, 229, 205)", "rgb(255, 242, 204)", "rgb(217, 234, 211)", 
			        "rgb(208, 224, 227)", "rgb(201, 218, 248)", "rgb(207, 226, 243)", "rgb(217, 210, 233)", "rgb(234, 209, 220)", 
			        "rgb(221, 126, 107)", "rgb(234, 153, 153)", "rgb(249, 203, 156)", "rgb(255, 229, 153)", "rgb(182, 215, 168)", 
			        "rgb(162, 196, 201)", "rgb(164, 194, 244)", "rgb(159, 197, 232)", "rgb(180, 167, 214)", "rgb(213, 166, 189)", 
			        "rgb(204, 65, 37)", "rgb(224, 102, 102)", "rgb(246, 178, 107)", "rgb(255, 217, 102)", "rgb(147, 196, 125)", 
			        "rgb(118, 165, 175)", "rgb(109, 158, 235)", "rgb(111, 168, 220)", "rgb(142, 124, 195)", "rgb(194, 123, 160)",
			        "rgb(166, 28, 0)", "rgb(204, 0, 0)", "rgb(230, 145, 56)", "rgb(241, 194, 50)", "rgb(106, 168, 79)",
			        "rgb(69, 129, 142)", "rgb(60, 120, 216)", "rgb(61, 133, 198)", "rgb(103, 78, 167)", "rgb(166, 77, 121)",
			        "rgb(91, 15, 0)", "rgb(102, 0, 0)", "rgb(120, 63, 4)", "rgb(127, 96, 0)", "rgb(39, 78, 19)", 
			        "rgb(12, 52, 61)", "rgb(28, 69, 135)", "rgb(7, 55, 99)", "rgb(32, 18, 77)", "rgb(76, 17, 48)"]
			    ]
			});

			$('#editevent_id').attr('value', eventid);
			$('#editModuleModal').modal('toggle');
		});
	});
}