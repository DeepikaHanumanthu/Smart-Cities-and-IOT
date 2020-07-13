(define (problem Evac) 
        (:domain Shmae)
(:objects 
    ;actuators
    mtr - chutemotor
    b - buzzer
    l - light
    h - message
    f - floor
    mr1 - mail_report
)

(:init
    ;todo: put the initial state's facts and numeric values here
    (off mr1)
    ;(at-mail_report mr1 f)
    ;(at-chutemotor mtr f)
    (off1 b)
    ;(at-buzzer b f)
    (off2 l)
    (off3 mtr)
    ;(at-light l f)
    ;thresholds for sensors
    (= (threshold_piezo) 16)
    (= (piezo f) 15)
    (= (threshold_moisture) 580)
    (= (moisture f) 560)
    (= (threshold_gyro) 8)
    (= (gyro f) 6)
    (= (threshold_crack) 25)
    (= (crack f) 20)
    (= (threshold_gas) 800)
    (= (gas f) 1000)
    (= (threshold_flame) 1)
    (= (flame f) 1)
    (= (threshold_pir) 1)
    (= (pir f) 1)
)

(:goal (and
        (health-monitor)
        (evac-execute)
)
)
)
