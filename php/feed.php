<?php
//Find all the events
// $events = Event::find_all();
$eventList = array();            // Assemble list of all events here

    //  foreach($events as $event):

    //    $eventList[] = array(              // Add our event as the next element in the event list
    //         'id'    => (int) $event->id,
    //         'title' => $event->event_title,
    //         'start' => $event->start_date." ".$event->start_time,
    //         'end'   => $event->end_date." ".$event->end_time,
    //         'url'   => "event_detail.php"
    //     );         
    // endforeach;

    $eventList[] = array(              // Add our event as the next element in the event list
            'id'    => 12,
            'title' => 'My event',
            'start' => '2015-11-05',
            'end'   => '2015-11-05',
            'url'   => "event_detail.php"
        );         

        $eventList[] = array(              // Add our event as the next element in the event list
            'id'    => 13,
            'title' => 'Firework Night',
            'start' => '2015-11-05',
            'end'   => '2015-11-05',
            'url'   => "event_detail.php"
        );  

    echo json_encode($eventList);       // encode and output the whole list.
?>