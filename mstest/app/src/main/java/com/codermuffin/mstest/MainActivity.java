package com.codermuffin.mstest;

import com.codermuffin.mstest.R;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Set the layout defined in res/layout/activity_main.xml

        // Find the TextView with the ID "helloTextView" and set its text
        TextView helloTextView = findViewById(R.id.helloTextView);
        helloTextView.setText("Hello, World!");
    }
}

