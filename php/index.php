<?php include 'header.php'; ?>

    <!-- Main jumbotron for a primary marketing message or call to action -->
<!--     <div class="jumbotron">
        <div class="container">
            <h1>Hello, world!</h1>
            <p>This is a template for a simple marketing or informational website. It includes a large callout called a jumbotron and three supporting pieces of content. Use it as a starting point to create something more unique.</p>
            <p><a class="btn btn-primary btn-lg" href="#" role="button">Learn more &raquo;</a></p>
            </div>
    </div> -->

    <br><br>

    <div class="container">
        <div class="row">
            <div class="col-xs-12">
                <div class="btn-group" role="group" aria-label="...">
                  <button type="button" class="btn btn-default">Module Timetable</button>
                  <button type="button" class="btn btn-default">Events</button>
                  <button type="button" class="btn btn-default">Deadlines</button>
                  <button type="button" class="btn btn-default">Group Work Deadlines</button>
                </div>
            </div>
        </div>

        <br>

        <div class="row">
            <div class="col-xs-9">
                <div id='calendar'></div>
            </div>
            <div class="col-xs-3">

                <div class="panel panel-default">
                  <div class="panel-heading">Add/ edit contents</div>
                  <div class="panel-body">
                    <ul>
                        <li><a href="#">Add modules</a></li>
                        <li><a href="#">Add events</a></li>
                        <li><a href="#">Add assignment</a></li>
                    </ul>
                  </div>
                </div>

                <div class="panel panel-default">
                  <div class="panel-heading">Group Hub</div>
                  <div class="panel-body">
                    <ul>
                        <li><a href="#">Group 1</a></li>
                        <li><a href="#">Group 2</a></li>
                        <li><a href="#">Group 3</a></li>
                    </ul>
                  </div>
                </div>

                <div class="panel panel-default">
                  <div class="panel-heading">Deadlines</div>
                  <div class="panel-body">
                    <ul>
                        <li>Deadline 1 - 10/10/2015</li>
                        <li>Deadline 2 - 16/11/2015</li>
                        <li>Deadline 3 - 25/12/2015</li>
                    </ul>
                  </div>
                </div>

            </div>
        </div>
        
    </div>



<?php include 'footer.php'; ?>