def get_deadlift_data(user, strength_record_label):

    deadlift_data = []

    for entry in strength_record_label:
        def check_if_entry_has_been_made(variable):
            for deadlift_record in StrengthRecords.objects.filter(user=user, exercise='Deadlift'):
                if variable == deadlift_record.date_of_record.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        deadlift_data.append(deadlift_record.weight_record * 2.20462)
                    else:
                        deadlift_data.append(deadlift_record.weight_record)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            deadlift_data.append('null')

    if user.weight_preference == 'LBS':
        deadlift_data[-1] = user.deadlift_record * 2.20462
    else:
        deadlift_data[-1] = user.deadlift_record

    return deadlift_data


def get_bench_press_data(user, strength_record_label):

    bench_press_data = []

    for entry in strength_record_label:
        def check_if_entry_has_been_made(variable):
            for bench_press_record in StrengthRecords.objects.filter(user=user, exercise='Bench Press'):
                if variable == bench_press_record.date_of_record.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        bench_press_data.append(bench_press_record.weight_record * 2.20462)
                    else:
                        bench_press_data.append(bench_press_record.weight_record)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            bench_press_data.append('null')

    #Puts the last data entry to current record
    if user.weight_preference == 'LBS':
        bench_press_data[-1] = user.bench_press_record * 2.20462
    else:
        bench_press_data[-1] = user.bench_press_record


    return bench_press_data


def get_squat_data(user, strength_record_label):

    squat_data = []
    for entry in strength_record_label:
        def check_if_entry_has_been_made(variable):
            for squat_record in StrengthRecords.objects.filter(user=user, exercise='Squat'):
                if variable == squat_record.date_of_record.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        squat_data.append(squat_record.weight_record * 2.20462)
                    else:
                        squat_data.append(squat_record.weight_record)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            squat_data.append('null')

    if user.weight_preference == 'LBS':
        squat_data[-1] = user.squat_record * 2.20462
    else:
        squat_data[-1] = user.squat_record



    return squat_data


def get_overhead_press_data(user, strength_record_label):

    overhead_press_data = []
    for entry in strength_record_label:
        def check_if_entry_has_been_made(variable):
            for overhead_press_record in StrengthRecords.objects.filter(user=user, exercise='Overhead Press'):
                if variable == overhead_press_record.date_of_record.strftime('%d%m'):
                    if user.weight_preference == 'LBS':
                        overhead_press_data.append(overhead_press_record.weight_record * 2.20462)
                    else:
                        overhead_press_data.append(overhead_press_record.weight_record)
                    return True

        if check_if_entry_has_been_made(entry) is not True:
            overhead_press_data.append('null')

    if user.weight_preference == 'LBS':
        overhead_press_data[-1] = user.overhead_press_record * 2.20462
    else:
        overhead_press_data[-1] = user.overhead_press_record

    return overhead_press_data


#deadlift_data = process.get_deadlift_data(user, strength_record_label)
    #bench_press_data = process.get_bench_press_data(user, strength_record_label)
    #squat_data = process.get_squat_data(user, strength_record_label)
    #overhead_press_data = process.get_overhead_press_data(user, strength_record_label)



<div class="container">
                    <div class="row">
                        <div class="col">
                            <h5>&nbsp</h5>
                            <h5>Weight:</h5>
                            <h5>Deadlift:</h5>
                            <h5>Bench(P)</h5>
                            <h5>Squat:</h5>
                            <h5>Overhead(P):</h5>
                        </div>
                          <div class="col">
                            <h5><strong>Current</strong></h5>
                            <h5>{{user.current_weight}} {{user.weight_preference}}</h5>
                            <h5>{{user.deadlift_record}} {{user.weight_preference}}</h5>
                            <h5>{{user.bench_press_record}} {{user.weight_preference}}</h5>
                            <h5>{{user.squat_record}} {{user.weight_preference}}</h5>
                            <h5>{{user.overhead_press_record}} {{user.weight_preference}}</h5>
                          </div>
                        <div class="col">
                            <h5><strong>Target</strong></h5>
                            <h5>{{user.weight_target}} KG</h5>
                            <h5>{{user.deadlift_target}} KG</h5>
                            <h5>{{user.bench_press_target}} KG</h5>
                            <h5>{{user.squat_target}} KG</h5>
                            <h5>{{user.overhead_press_target}} KG</h5>
                          </div>
                        <div class="col">
                            <h5><strong>Difference</strong></h5>
                            <h5 id="weight_difference"></h5>
                            <h5 id="deadlift_difference"></h5>
                            <h5 id="bench_press_difference"></h5>
                            <h5 id="squat_difference"></h5>
                            <h5 id="overhead_press_difference"></h5>

                            <script>
                                document.getElementById("deadlift_difference").innerHTML = (({{user.deadlift_target}} - {{user.deadlift_record}}) + " {{user.weight_preference}}")
                                document.getElementById("bench_press_difference").innerHTML = (({{user.bench_press_target}} - {{user.bench_press_record}}) + " {{user.weight_preference}}")
                                document.getElementById("squat_difference").innerHTML = (({{user.squat_target}} - {{user.squat_record}}) + " {{user.weight_preference}}")
                                document.getElementById("overhead_press_difference").innerHTML = (({{user.overhead_press_target}} - {{user.overhead_press_record}}) + " {{user.weight_preference}}")
                            </script>
                        </div>
                    </div>
                </div>

document.getElementById("weight_difference").innerHTML = (({{user.weight_target}} - {{user.current_weight}}) + " {{user.weight_preference}}")
document.getElementById("deadlift_difference").innerHTML = (({{user.deadlift_target}} - {{user.deadlift_record}}) + " {{user.weight_preference}}")
document.getElementById("bench_press_difference").innerHTML = (({{user.bench_press_target}} - {{user.bench_press_record}}) + " {{user.weight_preference}}")
document.getElementById("squat_difference").innerHTML = (({{user.squat_target}} - {{user.squat_record}}) + " {{user.weight_preference}}")
document.getElementById("overhead_press_difference").innerHTML = (({{user.overhead_press_target}} - {{user.overhead_press_record}}) + " {{user.weight_preference}}")