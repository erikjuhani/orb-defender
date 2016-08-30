class Clock:
    def __init__(self, hours, minutes, speed, sun_delay):
        self.days = 1
        self.hours = hours
        self.minutes = minutes
        self.speed = speed
        self.sun_delay = sun_delay # How long the sunrise or sunset lasts in game hours

    def tick(self, dt):
        self.minutes += self.speed * dt
        if self.minutes > 59:
            self.hours += 1
            self.minutes = 0
            if self.hours > 23:
                self.hours = 0
                self.days += 1

    def __str__(self):
        pM = pH = ""
        if self.minutes < 10:
            pM = "0"
        if self.hours < 10:
            pH = "0"
        return "Day: " + str(self.days) + " " + pH + str(self.hours) + ":" + pM + str(int(self.minutes))
