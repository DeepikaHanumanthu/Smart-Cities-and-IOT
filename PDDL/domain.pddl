;Header and description

(define (domain Shmae)

;remove requirements that are not needed
(:requirements :strips :fluents :typing :negative-preconditions :disjunctive-preconditions :equality)

(:types 
floor 
chutemotor 
light 
buzzer 
mail_report 
message
;todo: enumerate types and their hierarchy here, e.g. car truck bus - vehicle
;types of inputs- sensors of various types, various rooms and floors
;sensor
;types for actuators/outputs
)

; un-comment following line if constants are needed
;(:constants )

(:predicates ;todo: define predicates here
        (health-monitor)
        (evac-execute)
        (off ?mr1 - mail_report)
        (off1 ?b - buzzer)
        (off2 ?l - light)
        (off3 ?mtr - chutemotor)
        ;(at-buzzer ?b - buzzer ?f - floor)
        ;(at-light ?l - light ?f - floor)
        ;(at-chutemotor ?mtr - chutemotor ?f - floor)
        ;(at-mail_report ?mr1 - mail_report ?f -floor)
        (send ?h - message)

)


(:functions ;todo: define numeric functions here

        (piezo ?f - floor)
        (moisture ?f - floor)
        (gyro ?f - floor)
        (crack ?f - floor)
        (gas ?f - floor)
        (pir ?f - floor)
        (flame ?f - floor)
            (threshold_crack)
            (threshold_piezo)
            (threshold_moisture)
            (threshold_gyro)
            (threshold_gas)
            (threshold_flame)
            (threshold_pir)

)


(:action send-mail
    :parameters (?f - floor ?h - message ?mr1 - mail_report)
    :precondition (and (off ?mr1)
                  (>(piezo ?f) (threshold_piezo)) 
                  (>(moisture ?f) (threshold_moisture)) 
                  (>(gyro ?f) (threshold_gyro))
                  (>(crack ?f)(threshold_crack)))
    :effect (and (not(off ?mr1))(send ?h)(health-monitor))
)

(:action all-in-control
    :parameters (?f - floor ?h - message ?mr1 - mail_report)
    :precondition (or (<(piezo ?f) (threshold_piezo))
                  (<(moisture ?f) (threshold_moisture)) 
                  (<(gyro ?f) (threshold_gyro))
                  (<(crack ?f)(threshold_crack)))
    :effect (and (off ?mr1)(send ?h)(health-monitor))
)


(:action notify-emergency
    :parameters (?f -floor ?h - message ?mtr - chutemotor ?b - buzzer ?l - light)
    :precondition (and (off3 ?mtr) (off1 ?b) (off2 ?l)
                  (>(gas ?f) (threshold_gas))
                  (<(flame ?f)(threshold_flame))
                  (<(pir ?f)(threshold_pir)))
    :effect (and (not(off3 ?mtr)) (not(off1 ?b)) (not(off2 ?l)) (send ?h)(evac-execute))
)

(:action safe-state-no-emergency
    :parameters (?f -floor ?h - message ?mtr - chutemotor ?b - buzzer ?l - light)
    :precondition (or(<(gas ?f) (threshold_gas))
                  (=(flame ?f)(threshold_flame))
                  (=(pir ?f)(threshold_pir)))
     :effect (and (off3 ?mtr) (off1 ?b) (off2 ?l) (send ?h)(evac-execute))
)
)