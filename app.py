from flask import Flask, request, jsonify

app = Flask(__name__)

# Текущее положение сервопривода
servo_angle = 90


@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>ESP32 Servo</title>

        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                padding-top: 50px;
                background: #111;
                color: white;
            }

            h1 {
                font-size: 32px;
            }

            #angle {
                font-size: 50px;
                margin: 30px;
            }

            input {
                width: 80%;
                max-width: 500px;
            }

            button {
                font-size: 20px;
                padding: 15px 25px;
                margin: 10px;
            }
        </style>
    </head>

    <body>

        <h1>ESP32 SERVO</h1>

        <div id="angle">90°</div>

        <input
            type="range"
            min="0"
            max="180"
            value="90"
            id="slider"
        >

        <br><br>

        <button onclick="setAngle(0)">0°</button>
        <button onclick="setAngle(90)">90°</button>
        <button onclick="setAngle(180)">180°</button>

        <script>

            const slider = document.getElementById("slider");
            const angleText = document.getElementById("angle");

            slider.oninput = function() {

                angleText.innerHTML = this.value + "°";

                fetch("/set?angle=" + this.value);

            };


            function setAngle(angle) {

                slider.value = angle;

                angleText.innerHTML = angle + "°";

                fetch("/set?angle=" + angle);

            }

        </script>

    </body>
    </html>
    """


@app.route("/set")
def set_angle():

    global servo_angle

    try:
        angle = int(request.args.get("angle", 90))

        if angle < 0:
            angle = 0

        if angle > 180:
            angle = 180

        servo_angle = angle

        print("New servo angle:", servo_angle)

        return jsonify({
            "ok": True,
            "angle": servo_angle
        })

    except:
        return jsonify({
            "ok": False
        }), 400


@app.route("/get")
def get_angle():

    return jsonify({
        "angle": servo_angle
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=10000
    )
