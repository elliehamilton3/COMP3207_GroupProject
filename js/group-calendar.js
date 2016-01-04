$( document.body ).on( 'click', '.dropdown-menu li', function( event ) {

	 var $target = $( event.currentTarget );

	 $target.closest( '.btn-group' )
			.find( '[data-bind="label"]' ).text( $target.text() )
				 .end()
			.children( '.dropdown-toggle' ).dropdown( 'toggle' );

	 return false;

});

// Validation for input fields 
function validateEventInputs($edit) {
	if( $edit ) {
		$form = document.forms["editEventForm"];
	} else {
		$form = document.forms["addEventForm"];
	}
	
	var addEventEventName = $form["eventName"].value;
	var addEventLocation = $form["eventLocation"].value;
	var addEventStartDate = $form["start_date"].value;
	var addEventEndDate = $form["end_date"].value;
	var addEventStartTime = $form["start_time"].value;
	var addEventEndTime = $form["end_time"].value;

	if (addEventEventName == null || addEventEventName == "") {
		alert("Event name must be filled out");
		return false;
	}
	if (addEventEventName.length > 255) {
		alert("Event name is too long, please enter a shorter name");
		return false;
	}
	if (addEventLocation == null || addEventLocation == "") {
		alert("Event location must be filled out");
		return false;
	} 
	if (addEventLocation.length > 255) {
		alert("Event location is too long, please enter a shorter location name");
		return false;
	}
	if (addEventStartDate == null || addEventStartDate == "") {
		alert("Start date must be selected");
		return false;
	} 
	if (addEventEndDate == null || addEventEndDate == "") {
		alert("End date must be selected");
		return false;
	} 
	
	var split = addEventStartDate.split("/");
	var startDate = new Date(split[2], split[1] - 1, split[0]);
	
	var split = addEventEndDate.split("/");
	var endDate = new Date(split[2], split[1] - 1, split[0]);
	
	
	if (startDate > endDate) {
		alert("End date should be after the start date");
		return false;
	}
	if (addEventStartTime == null || addEventStartTime == "") {
		alert("Start time must be selected");
		return false;
	} 
	if (addEventEndTime == null || addEventEndTime == "") {
		alert("End time must be selected");
		return false;
	} 
	if (addEventStartDate == addEventEndDate && addEventStartTime>addEventEndTime){
		alert("If the start date and the end date are the same, the start time must be before the end time");
		return false;
	}
	
}

function validateTaskInputs() {
	var addTaskTaskName = document.forms["addTaskForm"]["taskName"].value;
	var addTaskDeadlineDate = document.forms["addTaskForm"]["deadline_date"].value;
	var addTaskDeadlineTime = document.forms["addTaskForm"]["deadline_time"].value;

	if (addTaskTaskName == null || addTaskTaskName == "") {
		alert("Task name must be filled out");
		return false;
	}
	if (addTaskTaskName.length > 255) {
		alert("Task name is too long, please enter a shorter name");
		return false;
	}
	/*if (addTaskDeadlineDate == null || addTaskDeadlineDate == "") {
		alert("Date must be selected");
		return false;
	}
	if (addTaskDeadlineTime == null || addTaskDeadlineTime == "") {
		alert("Time must be selected");
		return false;
	}*/
}
function validateEditGroupInputs() { 	
	var editGroupGroupName = document.forms["editGroupForm"]["group_name"].value;
	var editGroupDescription = document.forms["editGroupForm"]["group_description"].value;		

	if (editGroupGroupName == null || editGroupGroupName == "") {
		alert("Group name must be filled out");
		return false;
	}
	if (editGroupGroupName.length > 255) {
		alert("Group name is too long, please enter a shorter name");
		return false;
	}  					
	if (editGroupDescription == null || editGroupDescription == "") {
		alert("Group description must be filled out");
		return false;
	}
	if (editGroupDescription.length  > 255) {
		alert("Group description is too long, please enter a shorter name");
		return false;
	} 
}

function cancelDeleteTask(id) {
	location.reload();
}
					
function deleteEvent(id) {
	alert("Event DELETED: " + id);
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
