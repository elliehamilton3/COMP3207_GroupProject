function signOut() {
	var auth2 = gapi.auth2.getAuthInstance();
	auth2.signOut().then(function () {
		console.log('User signed out.');
	});
}

// Needs to be within the HTML
$(document).ready(function() {
	{% if user.name == None %}
		$('#nameModal').modal('show');
	{% endif %}
});

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
			
function validateAddGroupInputs() { 	
	var addGroupGroupName = document.forms["addGroupForm"]["group_name"].value;
	var addGroupDescription = document.forms["addGroupForm"]["group_description"].value;
	

	if (addGroupGroupName == null || addGroupGroupName == "") {
		alert("Group name must be filled out");
		return false;
	}
	if (addGroupGroupName.length > 255) {
		alert("Group name is too long, please enter a shorter name");
		return false;
	}  					
	if (addGroupDescription == null || addGroupDescription == "") {
		alert("Group description must be filled out");
		return false;
	}
	if (addGroupDescription.length > 255) {
		alert("Group description is too long, please enter a shorter name");
		return false;
	} 
}		

function validateKeyInputs($edit) {
	if( $edit ) {
		$form = document.forms["editKeyForm"];
	} else {
		$form = document.forms["addKeyForm"];
	}
	
	var keyName = $form["name"].value;

	if (keyName == null || keyName == "") {
		alert("Key name must be filled out");
		return false;
	}
	if (keyName.length > 255) {
		alert("Key name is too long, please enter a shorter name");
		return false;
	}
}
