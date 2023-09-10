import gunController
from time import sleep

nem = gunController.Nemesis()

print("revving")
nem.rev()

sleep(2)

print("unrevving")
nem.unrev()

sleep(2)

print("revving and shooting")
nem.rev()
sleep(1)
nem.shoot()

print("turning off")
nem.off()