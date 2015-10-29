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
            <div class="col-xs-9">
                <div class="btn-group btn-group-justified" role="group" aria-label="...">
                    <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Module Timetable</button>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Events</button>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Deadlines</button>
                  </div>
                  <div class="btn-group" role="group">
                    <button type="button" class="btn btn-default">Group Work Deadlines</button>
                  </div>
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
                      <li><a href="#" data-toggle="modal" data-target="#addModuleModal">Add modules</a></li>

                      <!-- Modal -->
                      <div id="addModuleModal" class="modal fade" role="dialog">
                        <div class="modal-dialog">

                          <!-- Modal content-->
                          <div class="modal-content">
                            <div class="modal-header">
                              <button type="button" class="close" data-dismiss="modal">&times;</button>
                              <h4 class="modal-title">Add Modules</h4>
                            </div>
                            <div class="modal-body">

                              
                              <!-- Form within Modal -->
                              <form class="form-horizontal" role="form">
                                <div class="dropdown">
                                  <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
                                    Dropdown
                                    <span class="caret"></span>
                                  </button>
                                  <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
                                    <li><a href="#">Module 1</a></li>
                                    <li><a href="#">Module 2</a></li>
                                    <li><a href="#">Module 3</a></li>
                                    <li><a href="#">Module 4</a></li>
                                  </ul>
                                </div>
                                <div class="form-group"> 
                                  <div class="col-sm-11">
                                    <button type="submit" class="btn btn-default pull-right">Submit</button>
                                  </div>
                                </div>
                              </form>
                              <!-- //Form within Modal -->


                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            </div>
                          </div>
                          <!-- //Modal Content -->
                        </div>
                      </div>
                      <!-- //Modal -->


                      <li><a href="#" data-toggle="modal" data-target="#addEventsModal">Add events</a></li>
                      <!-- Modal -->
                      <div id="addEventsModal" class="modal fade" role="dialog">
                        <div class="modal-dialog">

                          <!-- Modal content-->
                          <div class="modal-content">
                            <div class="modal-header">
                              <button type="button" class="close" data-dismiss="modal">&times;</button>
                              <h4 class="modal-title">Add Events</h4>
                            </div>
                            <div class="modal-body">
                              <p>Some text in the modal.</p>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            </div>
                          </div>
                          <!-- //Modal Content -->
                        </div>
                      </div>
                      <!-- //Modal -->


                      <li><a href="#" data-toggle="modal" data-target="#addAssignmentModal">Add assignment</a></li>
                      <!-- Modal -->
                      <div id="addAssignmentModal" class="modal fade" role="dialog">
                        <div class="modal-dialog">

                          <!-- Modal content-->
                          <div class="modal-content">
                            <div class="modal-header">
                              <button type="button" class="close" data-dismiss="modal">&times;</button>
                              <h4 class="modal-title">Add Assignments</h4>
                            </div>
                            <div class="modal-body">
                              <p>Some text in the modal.</p>
                            </div>
                            <div class="modal-footer">
                              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                            </div>
                          </div>
                          <!-- //Modal Content -->
                        </div>
                      </div>
                      <!-- //Modal -->
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