package com.example.morsetorch

import android.content.Context
import android.hardware.camera2.CameraManager
import android.os.Build
import android.os.Bundle
import android.text.InputType
import android.widget.*

import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatActivity
import kotlinx.android.synthetic.main.activity_main.*
import kotlinx.coroutines.*
import kotlinx.coroutines.Dispatchers.IO
import kotlin.coroutines.CoroutineContext



class MainActivity : AppCompatActivity() {

    private lateinit var camManager:CameraManager
    private lateinit var camId:String

    lateinit var statusbar:TextView
    lateinit var displayText:TextView
    lateinit var timeFactorText:TextView
    lateinit var inputtext:EditText

    lateinit var  mainButton:Button
    lateinit var cancelB:Button


    private lateinit var obj:CoroutineContext

    val signalTimeMap = mapOf<String,Long>(
        "0" to 1,
        "1" to 3,
        "2" to 1,
        "3" to 3,
        "4" to 7
    )


    var timeFactor:Float = 1F
    enum class Signaling{
        Stopped,Running
    }
    private var programState = Signaling.Stopped

    @RequiresApi(Build.VERSION_CODES.LOLLIPOP)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        camManager = getSystemService(Context.CAMERA_SERVICE) as CameraManager
        camId = camManager.cameraIdList[0]

        mainButton = findViewById<Button>(R.id.button_main)
        cancelB = findViewById<Button>(R.id.cancel)
        val seekbar = findViewById<SeekBar>(R.id.seekBar)

        statusbar = findViewById<TextView>(R.id.status_text)
        inputtext = findViewById<EditText>(R.id.inputText)
        timeFactorText = findViewById<TextView>(R.id.tud)
        displayText = findViewById<TextView>(R.id.displayText)

        //initial conditions
        timeFactorText.text = String.format("%.1f s",timeFactor )






        mainButton.setOnClickListener {

            var inputtext_str = ((inputtext.text).toString()).trim()

            if(inputtext_str != ""){
                programState = Signaling.Running

                updateStatus()

                obj = CoroutineScope(IO).launch {
                    lockUI()
                    var inputString = inputtext_str.toLowerCase()
                    test((convertToSignal(inputString)), inputString)
                }
            } else{
                Toast.makeText(this@MainActivity,"Yo, Type something!",Toast.LENGTH_SHORT).show()
            }
            


    }


        cancelB.setOnClickListener {
            programState = Signaling.Stopped
            updateStatus()
            obj.cancel()
            switchOnFlashLight(false)
            unlockUI()
        }

        seekbar?.setOnSeekBarChangeListener(object :
            SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seek: SeekBar, progress: Int, fromUser: Boolean) {
                //   code for progress is changed
                timeFactor = 0.1F*seek.progress.toFloat()
                timeFactorText.text = String.format("%.1f s",timeFactor )
            }

            override fun onStartTrackingTouch(seek: SeekBar) {
                //   code for progress is started
            }

            override fun onStopTrackingTouch(seek: SeekBar) {
                //   code for progress is stopped


            }
        })

    }

    private fun updateUI(msg:String){
        GlobalScope.launch(Dispatchers.Main){
            //delay(2000)
            displayText.text = msg


        }
    }

    private fun updateStatus(){
        GlobalScope.launch(Dispatchers.Main){
            statusbar.text = programState.toString()
            if (programState == Signaling.Stopped){
                displayText.text = ":)"
            }

        }
    }

    private fun lockUI(){
        GlobalScope.launch(Dispatchers.Main){
            inputtext.isFocusable = true
            inputtext.isFocusableInTouchMode = true
            inputtext.inputType = InputType.TYPE_NULL

            seekBar.isEnabled = false
            mainButton.isEnabled = false
            cancelB.isEnabled = true
        }

    }

    private fun unlockUI(){
        GlobalScope.launch(Dispatchers.Main){
            inputtext.isFocusable = true
            inputtext.isFocusableInTouchMode = true
            inputtext.inputType = InputType.TYPE_CLASS_TEXT

            seekBar.isEnabled = true
            mainButton.isEnabled = true
            cancelB.isEnabled = false
        }

    }




    private suspend fun test (signalSeq:String,wordSeq:String) {
        var j = 0
        for ((iId,i) in signalSeq.withIndex()){


            if (iId> 0){
                if ((signalSeq[iId-1].toString() == "3") || (signalSeq[iId].toString() == "4") || (signalSeq[iId-1].toString() == "4")){
                    j +=1
                }
            }


            updateUI(wordSeq[j].toString())

            when(i.toString()){
                "0" -> switchOnFlashLight(true)
                "1" -> switchOnFlashLight(true)
                "2" -> switchOnFlashLight(false)
                "3" -> switchOnFlashLight(false)
                "4" -> switchOnFlashLight(false)
            }
            delay ((1000*timeFactor*signalTimeMap.getValue(i.toString())).toLong())}

        //updateUI()

        programState = Signaling.Stopped
        switchOnFlashLight(false)
        updateStatus()
        unlockUI()

    }




    @RequiresApi(Build.VERSION_CODES.M)
    fun switchOnFlashLight(status:Boolean){
        camManager.setTorchMode(camId,status)
    }







}
