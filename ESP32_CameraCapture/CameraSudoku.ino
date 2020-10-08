#include "esp_camera.h"
#include <WiFi.h>

// Select camera model
#define CAMERA_MODEL_AI_THINKER

#include "camera_pins.h"

const char* ssid = "****";
const char* password = "****";
const int buttonPin = 12;     // the number of the pushbutton pin

const String serverName = "192.168.100.4";
const String serverPath = "/api/upload";
const int serverPort = 5000;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  //init with high specs to pre-allocate larger buffers
  if(psramFound()){
    config.frame_size = FRAMESIZE_UXGA;
    config.jpeg_quality = 10;
    config.fb_count = 2;
  } else {
    config.frame_size = FRAMESIZE_SVGA;
    config.jpeg_quality = 12;
    config.fb_count = 1;
  }

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x", err);
    return;
  }

  //sensor_t * my_camera = esp_camera_sensor_get();

  WiFi.begin(ssid, password);

  pinMode(buttonPin, INPUT);
  Serial.print("Ready!\n");
}

bool SendPhoto(camera_fb_t *pic){
  if (client.connect(serverName.c_str(), serverPort)) {
    String head = "--SolveSudoku\r\nContent-Disposition: form-data; name=\"capture\"; filename=\"esp32-cam.jpg\"\r\nContent-Type: image/jpeg\r\n";
    String tail = "\r\n--SolveSudoku--\r\n";

    uint32_t imageLen = pic->len;
    uint16_t extraLen = head.length() + tail.length();
    uint32_t totalLen = imageLen + extraLen;
  
    client.println("POST " + serverPath + " HTTP/1.1");
    client.println("Host: " + serverName);
    client.println("Content-Length: " + String(totalLen));
    client.println("Content-Type: multipart/form-data; boundary=SolveSudoku");
    client.println();
    client.println(head);
  
    uint8_t *fbBuf = pic->buf;
    size_t fbLen = pic->len;
    for (size_t n=0; n<fbLen; n=n+1024) {
      if (n+1024 < fbLen) {
        client.write(fbBuf, 1024);
        fbBuf += 1024;
      }
      else if (fbLen%1024>0) {
        size_t remainder = fbLen%1024;
        client.write(fbBuf, remainder);
      }
    }   
    client.print(tail);
    client.stop();
    return true;
  }
  else {
    return false;
  }
}

void loop() {
  int buttonState = digitalRead(buttonPin);

  camera_fb_t *pic;
  if (buttonState == HIGH) {
    Serial.println("Taking photo");
    pic = esp_camera_fb_get();
    if(SendPhoto(pic)){
      Serial.print("...Sent photo");
      delay(2000);
    }
    else Serial.print("...Sending failed");
    esp_camera_fb_return(pic);
  }
  delay(800);
}
