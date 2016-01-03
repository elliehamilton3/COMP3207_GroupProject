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
			
			// If the minute is < 10, it is missing the leading 0
			if( start_minute < 10 ) {
				start_minute = "0" + start_minute;				
			}
			
			if( end_minute < 10 ) {
				end_minute = "0" + end_minute;
			}

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
    });
	$(".colorpicker").spectrum({
	    color: "gray",
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
	$('.datepicker').datepicker({format: 'dd/mm/yyyy'});

	function buildHtmlTable(selector) {
		$.getJSON( "/taskfeed", function( data ) {
		  var items = [];
		  var month = '';
		  $.each( data, function( key, val ) {
		  	if( val['month'] !== month ) {
		  		month = val['month'];
		  		items.push( "<div class='table-heading'>" + month + "</div>" );
		    }
		    
			items.push( "<li class='list-group-item' id='"+ val['id'] +"' data-style='button' data-color='"+ val['color'] +"'style='color:"+ val['color'] + "'>" + val['datetime'] + " " + val['title']  + "</li>" );
		  });
			if(items.length == 0){
				items.push( "<p class='no-tasks'>You have no tasks to do!</p>" );
			}
		  $( "<ul/>", {
		    "class": "list-group checked-list-box",
		    "id": "check-list-box",
		    html: items.join( "" )
		  }).appendTo(selector);

		  $(function () {
		    $('.list-group.checked-list-box .list-group-item').each(function () {
		        
		        // Settings
		        var $widget = $(this),
		            $checkbox = $('<input type="checkbox" class="hidden" />'),
		            color = ($widget.data('color') ? $widget.data('color') : "primary"),
		            style = ($widget.data('style') == "button" ? "btn-" : "list-group-item-"),
		            settings = {
		                on: {
		                    icon: 'glyphicon glyphicon-check'
		                },
		                off: {
		                    icon: 'glyphicon glyphicon-unchecked'
		                }
		            };
		            
		        $widget.css('cursor', 'pointer')
		        $widget.append($checkbox);

		        // Event Handlers
		        $widget.on('click', function () {
		            $checkbox.prop('checked', !$checkbox.is(':checked'));
		            updateDisplay();
		        });
		       
	          

		        // Actions
		        function updateDisplay() {
		            var isChecked = $checkbox.is(':checked');

		            // Set the button's state
		            $widget.data('state', (isChecked) ? "on" : "off");

		            // Set the button's icon
		            $widget.find('.state-icon')
		                .removeClass()
		                .addClass('state-icon ' + settings[$widget.data('state')].icon);

		            // Update the button's color
		            if (isChecked) {
		                
		                $widget.css({"background-color":color,"color":'black'});

						console.log($widget);
						console.log($checkbox);
						
						$('#modal-footer').empty().append('<button type="button" class="btn btn-default" data-dismiss="modal" onclick="cancelDeleteTask('+$widget.attr('id')+')">Cancel</button><a class="btn btn-danger btn-ok" id="taskdelete" onclick="deleteTask('+$widget.attr('id')+')">Delete</a>');
		                $('#confirm-delete').modal('toggle');
		                
		            } 
		            else {
		                
		                $widget.css({"background-color":"white","color":color});
		            }
		        }

		        // Initialization
		        function init() {
		            
		            if ($widget.data('checked') == true) {
		                $checkbox.prop('checked', !$checkbox.is(':checked'));
		            }
															
		            updateDisplay();

		            // Inject the icon if applicable
		            if ($widget.find('.state-icon').length == 0) {
		                $widget.prepend('<span class="state-icon ' + settings[$widget.data('state')].icon + '"></span>');
		            }
		        }
		        init();
	    	});
	    
		    $('#get-checked-data').on('click', function(event) {
		        event.preventDefault(); 
		        var checkedItems = {}, counter = 0;
		        $("#check-list-box li.active").each(function(idx, li) {
		            checkedItems[counter] = $(li).text();
		            counter++;
		        });
		        $('#display-json').html(JSON.stringify(checkedItems, null, '\t'));
		    });
		  });

		});
		
		
	}
	function buildDeadlinesBox(selector) {
		$.getJSON( "/taskboxfeed", function( data ) {
		  var items = [];
		  $.each( data, function( key, val ) {
		    items.push( "<li>" + val['datetime'] + " " + val['title']  + "</li>" );
		  });
		 
		  $( "<ul/>", {
		    "class": "",
		    "id": "",
		    html: items.join( "" )
		  }).appendTo(selector);

		  
		});
	}
	function buildGroupsList(selector) {
		$.getJSON( "/groupfeed", function( data ) {
		  var items = [];
		  $.each( data, function( key, val ) {
		    items.push( "<a href='/grouppage?group=" + val['key'] + "'><li class='list-group-item'>" + val['name']  + "<p class='group-desc'>" + val['description'] + '</p></li></a>' );
		  });
		 
			if(items.length == 0){
				items.push( "<li class='list-group-item'>You have no groups!</li>" );
			}
		 
		  $( "<ul/>", {
		    "class": "list-group",
		    "id": "groups-list",
		    html: items.join( "" )
		  }).appendTo(selector);

		  
		});
	}
	
	function getKeys() {
		$.getJSON( "/getkeys", function( data ) {
			var items = [];
			var modal_items = [];
			$.each( data, function( key, val ) {
				items.push( "<li>" + ' <span style="background-color:' + val['color'] + ';width:25px;height:10px;display:inline-block;margin-right:5px;"></span>' + val['name'] + '<a onClick="createEditKeyModal(\'' + val['key'] + "','" + val['name'] + "','" + val['color'] +'\')">Edit</a></li>' );
				modal_items.push("<option value='" + val['key'] + "'>" + val['name'] + "</option>");
			});
				 
			// Add to sidebar
			$( "<ul/>", {
				"class": "",
				"id": "",
				html: items.join( "" )
			}).appendTo('#keylist');
			
			// Add to modals
			$('#eventtype').append(modal_items.join(""));
			$('#editeventtype').append(modal_items.join(""));
			$('#tasktype').append(modal_items.join(""));
		});
	}

	buildHtmlTable('#excelDataTable');
	buildDeadlinesBox('#deadlinesbox');
	buildGroupsList('#grouplist');
	getKeys();
	//$('#confirm-delete').modal({ backdrop: 'static', keyboard: false });



});
function createEditModal(eventid) {
	$.getJSON( "/getevent?eventid="+eventid, function( data ) {
		$.each( data, function(key, val) {
			$('#editeventname').val(val['name']);
			$('#editeventtype').val(val['event_type']);
			$('#editeventlocation').val(val['location']);
			var startDate = val['start_time'].split("T")[0].split("/");
			var startTime = val['start_time'].split("T")[1];
			var start = new Date(startDate);

			var endDate = val['end_time'].split("T")[0].split("/");
			var endTime = val['end_time'].split("T")[1];
			var end = new Date(endDate);
			
			$('.editstartdate').datepicker({format: 'dd/mm/yyyy'}).datepicker("setDate", start);
			$('.editstarttime').timepicker({"defaultTime": startTime, minuteStep: 5, showMeridian: false, pick12HourFormat: false, format: 'HH:mm' });

			$('.editenddate').datepicker({format: 'dd/mm/yyyy'}).datepicker("setDate", end);
			$('.editendtime').timepicker({"defaultTime": endTime, minuteStep: 5, showMeridian: false, pick12HourFormat: false, format: 'HH:mm' });
			
			$('#editevent_id').attr('value', eventid);
			$('#editModuleModal').modal('toggle');
		});
	});
}

function createEditKeyModal(key, name, color) {
		$('#edit_key_name').val(name);
		$('#edit_key_id').val(key);
			
		$("#edit_key_color").spectrum({
			color: color,
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
		$('#edit_key_color').attr('value', color);
		$('#editKeyModal').modal('toggle');
}

function deleteTask(id) {
    var xhr = new XMLHttpRequest();
	xhr.open('POST', '/removetask');
	xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	xhr.onload = function() {
		location.reload();
	};
	xhr.send('taskid=' + id);
}
function cancelDeleteTask(id) {
	var li = document.getElementById(id);
	var checkbox = li.getElementsByTagName("input")[0];
	checkbox.checked = false;
	location.reload();
}
window.onload = function(){  

    var url = document.location.toString();
    if (url.match('#')) {
	    $('.nav a[href=#'+url.split('#')[1]+']').tab('show') ;
	} 

	// Change hash for page-reload
	$('.nav a').on('shown.bs.tab', function (e) {
	    window.location.hash = e.target.hash;
	});
} 