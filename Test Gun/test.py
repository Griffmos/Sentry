import gunController
from time import sleep

nem = gunController.Nemesis()

print("revving")
nem.rev()

sleep(5)

print("unrevving")
nem.unrev()

sleep(5)

print("revving and shooting")
nem.rev()
sleep(2)
nem.shoot()

sleep(5)

print("turning off")
nem.off()
