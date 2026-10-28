# Add project specific ProGuard rules here.
# You can control the set of applied configuration files using the
# proguardFiles setting in build.gradle.
#
# For more details, see
#   http://developer.android.com/guide/developing/tools/proguard.html

# If your project uses WebView with JS, uncomment the following
# and specify the fully qualified class name to the JavaScript interface
# class:
#-keepclassmembers class fqcn.of.javascript.interface.for.webview {
#   public *;
#}

# Uncomment this to preserve the line number information for
# debugging stack traces.
#-keepattributes SourceFile,LineNumberTable

# If you keep the line number information, uncomment this to
# hide the original source file name.
#-renamesourcefileattribute SourceFile

# --- Guardians of Gala ------------------------------------------------------------------------------
# Only used when a build sets -Pminify=true (R8 is off by default, see build.gradle). Capacitor ships its
# own consumer rules for plugins/bridge; these two cover the WebView bridge and readable crash stack traces.
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}
-keepattributes JavascriptInterface,*Annotation*,SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile
