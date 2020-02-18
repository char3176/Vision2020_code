# C-19/38 Mon 2020 02 17
  # RasPi
    - setup static IPs for eth0 that connect to robotRadio
      - One setup for @home (roboRio = 10.12.34.2)
      - One setup for @competition (roboRio = ??.31.76.??)
    - setup automatic execution of Vision code on boot/startup
      - cron job or systemd?  systemd, probably.
    - make sure raspi-cam + usb-fisheye can both run together on same pi
    - make sure ssh-server running by default and ports open
    - if time, implement web-front-end
    - create sd-image with no gui running
    - double-check "actual" fps with camera & video-in-video nesting
      trick for ALL cameras.

  # Vision master-loop
    - implement video stream server
      - ballPi feed should able to toggle between 
        pi-cam and usb-fisheye
        at driveStation
          usbcam -> vs = VideoStream(src=0).start()
      - g2Pi feed should be able to toggle reticle on and off
      - both ballPi and g2Pi should have pynetwork boolean that if set
        to False, no video feed is sent from Pi (to conserve bandwidth).
        If set to True, then video feed on Pi is packaged into
        pynetworktable and sent to driveStation.  
          - Should driveStation have one video window with 3 feeds, or
            two video windows - one for g2Pi's single feed, and one for
            ballPi's two feeds?
    - add heartbeat to visionServer and visionClient.java
    - add proper logging statements through-out
    - add "snap pic" functionality:  driverStation clicks button and 
      Pi takes/saves quick series of snapshots (say, 9 pics evenly 
      spread out over 300 ms - essentially 1 pic per each 20-40ms
      loop of robotInit? Or maybe longer - 50 pics over 1000 ms, 
      1 each per 20-40ms loop?  These "1 per 20-40ms loop" are useful 
      for debugging, but won't be very good for PR, so maybe have 
      another "snap pic" version/option that grabs 1 pic every 100ms 
      over 5 sec for a total of 50 pics?)
    - Or hell, worst case, have a "save all frames" fxn that 
      saves every
      frame while SaveAllFrames = True.
    - add "rec vid" functionality:  driverStation clicks button and Pi
      takes short video (say, 10 sec?) and stores on disk
    - add shutdown command so that driveStation can tell rPi to
      "shutdown now"
    
  # NetworkTables
    - add these to ballTable / g2Table:
      - image width
      - image height
      - image fps
      - heartbeat
      - rec vid
      - snap pics
      - saveAllFrames
      - toggle vid feed on/off
      - "stop image processing" signal that stops costly 
        vision processing part of visionServer loop? (Also have 
        "start image processing" to restart it?  Image processing 
        should be on by default at boot/startup.)
      - "shutdown now" signal for Rpi turning off rpi from 
        driveStation
    - add these to ballTable
      - toggle vid feed source (for ball vs fisheye feeds on ballPi)
      - target_data array/packet for ballToChase
    - add these to g2Table
      - toggle reticle on/off (for g2 vid feed)
      - boolean that if True, turns on LEDs; if False, turns off LEDs
      - target_data array/packet for G2


  # G2
    - add reticle change color if isInROF=True
    - if time, add full solvePNP

  # LB
    - copy G2 and apply LB geom
      - still not clear why we'd want to know LB location.....?

  # ball
    - try supervise.ly
      - get dataset
      - label dataset
        - These as the classes? : fullBall, ballAggregate, 
          occludedBall, noBall
      - inquire of Nathan about AWS credits

  # sw_arch
    - intro command-based programming to stuart
    - map-out sys arch and subsys arch
    - 

  # ifNoTurrent
    - divide goal-side of field into sectors/quads
    - create traj's in pathweaver from each sector to "launch area"
      sectors
    - figure out how to deal with determining initial orientation.  
      Maybe spin in place until camera acquisition of G2 and LB, then 
      triangulate my sector using distance-to-G2, distance-to-LB, 
      angle-to-G2, and angle-to-LB. Then engage a pathfinder traj 
      to a "launch area" sector.

  # ifTurrent
    - determine if ever need to know/track relative rotation of turret
      to chassis.
        - YES: if engaging automated drive/traj based on 
          data/pic from turret cam.


   




  
