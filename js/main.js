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
		 }

		 // events: [
   //      {
   //          title  : 'event1',
   //          start : '2015-11-05T09:20:22+00:00',
	  //       end : '2015-11-05T17:20:22+00:00'
   //      }
	  //   ]

    })

});