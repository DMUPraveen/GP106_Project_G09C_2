package com.example.morsetorch

val toInputData = mapOf<String,String>(
      "." to "0",
      "-" to "1",
      ""  to "2",
      "," to "3",
      " " to "4"
)

val toMorse = mapOf<String,String>(

    // Letters
        "a" to  ".-",
        "b" to  "-...",
        "c" to  "-.-.",
        "d" to  "-..",
        "e" to  ".",
        "f" to  "..-.",
        "g" to  "--.",
        "h" to  "....",
        "i" to  "..",
        "j" to  ".---",
        "k" to  "-.-",
        "l" to  ".-..",
        "m" to  "--",
        "n" to  "-.",
        "o" to  "---",
        "p" to  ".--.",
        "q" to  "--.-",
        "r" to  ".-.",
        "s" to  "...",
        "t" to  "-",
        "u" to  "..-",
        "v" to  "...-",
        "w" to  ".--",
        "x" to  "-..-",
        "y" to  "-.--",
        "z" to  "--..",
    // Numbers
        "0" to  "-----",
        "1" to  ".----",
        "2" to  "..---",
        "3" to  "...--",
        "4" to  "....-",
        "5" to  ".....",
        "6" to  "-....",
        "7" to  "--...",
        "8" to  "---..",
        "9" to  "----.",
    //Punctuation
        "&" to  ".-...",
        "'" to  ".----.",
        "@" to  ".--.-.",
        ")" to  "-.--.-",
        "(" to  "-.--.",
        ":" to  "---...",
        "," to  "--..--",
        "=" to  "-...-",
        "!" to  "-.-.--",
        "." to  ".-.-.-",
        "-" to  "-....-",
        "+" to  ".-.-.",
        '"'.toString() to  ".-..-.",
        "?" to  "..--..",
        "/" to  "-..-.",
        " " to  " "    // <---- additional entry
)

fun _englishToMorse_(wordSeq:String): MutableList<String> {
    var translated:MutableList<String> = mutableListOf()

    for (char in wordSeq){
        translated.add(toMorse.getValue(char.toString()))
    }

    return translated
}

fun _morseToSignal_(morse:MutableList<String>): String {

    var mtranslated:MutableList<String> = mutableListOf()

    for ((iID:Int,i:String) in morse.withIndex()){
        for ((jID:Int,j:Char) in i.withIndex()){
            mtranslated.add(toInputData.getValue(j.toString()))
            if (jID != i.length-1){
                mtranslated.add("2")
            }
        }
        if ((iID < morse.size-1) && (i != " ") && (morse[iID+1] != " ")){
            mtranslated.add("3")
        }
    }



    return mtranslated.joinToString(prefix = "",postfix = "",separator = "")
}

fun convertToSignal(words:String): String {
    return _morseToSignal_(_englishToMorse_(words))
}