/*----------------------------------------------------------------------------*/
/* Copyright (c) 2018-2019 FIRST. All Rights Reserved.                        */
/* Open Source Software - may be modified and shared by FRC teams. The code   */
/* must be accompanied by the FIRST BSD license file in the root directory of */
/* the project.                                                               */
/*----------------------------------------------------------------------------*/

package frc.robot;

import edu.wpi.first.networktables.*;

/**
 * Add your docs here.
 */
public class VisionClient {
        /*--------------------------------------------------------------
         * CHAR_FLAG: RETURN_FOR_CLEANUP_PRI2  ... may resolve itself.
         * DETAILS:
         *      Something seems off here...but haven't yet precisely put
         * finger on it.  Unclear how VisionClient in current form could
         * satisfy Init & Periodic phases' execution requirements.
         * There's no Command Scheduling. For that matter, there's no 
         * Scheduler at all. Even pseudo-scheduler loopManager is absent. 
         * No callbacks involved AFAICT.
        /*--------------------------------------------------------------*/

        /* ---------- */
        /* Init Stuff */
        /* ---------- */
        NetworkTableInstance instance = NetworkTableInstance.getDefault();
        NetworkTable fuTable = instance.getTable("fuVision");

        /* -------------- */
        /* Periodic Stuff */
        /* -------------- */
        double[] fuTargetData = fuTable.getEntry("target_data").getDoubleArray(defaultValue);
        /*--------------------------------------------------------------
         * This note explains received "target_data" format.
         * DETAIL:
         *      NetworkTablesEntry "fuVision/target_data" is an
         * ARRAY that holds the data needed to autonomously "chase
         * the ball."
         *      We tx/rx as an array to insure the time-relevant data
         * is sent and received together in a packet, to prevent
         * fractional knowledge states between asynchronous msg handlers.
         *      The array's values are FLOATS as required by 
         * NetworkTables. Elements of the array represent, in 
         * the following order: 
         *   Timestamp: time record at which image was acquired on 
         *              co-processor
         *   isFound:   0.0 = no Ball present, 1.0 = a Ball is present
         *   Mode: 
         *   distance:  euclidean distance in meters to detected Ball
         *   yaw:       horizontal angle to detected ball where center 
         *              pixel of image has angle of 0.0
        /*--------------------------------------------------------------*/

        public boolean isBallTargetAvail() {
            return fuTargetData[2];
        }

        public double getBallDistance() {
            return fuTargetData[4];
        }

        public double getBallAngle() {
            return fuTargetData[5];
        }
        

}
