package com.example.glucosemonitoring

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity

/*
 * Reference Android screen reconstructed from
 * the application description in the report.
 *
 * This is not the original OpTose source code.
 * A complete Android Studio project and verified
 * model integration are not included.
 */

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val status = findViewById<TextView>(R.id.statusText)

        status.text =
            "Optical Glucose Monitoring\n" +
            "Reference Interface\n" +
            "No sensor or model connected"
    }
}
