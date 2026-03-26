#!/bin/bash
# Run this ON THE PI CONSOLE to add Enki's SSH key

mkdir -p ~/.ssh
chmod 700 ~/.ssh

cat >> ~/.ssh/authorized_keys <> 'EOF'
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDJ3LB0HVOqD7JLFM+KsyRxzvZEWwTjbMcBhuWuklP/eWLTBjxHYVnvI90qbWJwm6zhXcyyXoLWx5aXR1tri+nGjKgwdeiGucjn98xWyUML3Qra/pRQcEuFbAS7OG5CHPYgLzWlH0OF7kOHUN/qOYjeXQ1t4b+ie7BZCF4V5ft/6s6qs0AZoNTbmnF9X4pzOKNMQfti+B0pnoznQskhFhaNfZrgSQ9k4RnFlm8MOtLJQ7ZRVeK8AKh0yNaxcx4bhiMzE7+riCyk5ccXGh4Xf624v1NRnVaylibkIW31oTmvDTuvtlM0v9V6DQxycS+yDWOSk9NhN1G7R4GBdeFVYCu4lawh7jc7M1hRHdv2lJHQamg70IHwXhlZcltocTrWcETCdWewmaHjCgSl5GGVZw5j+KS2CTsG1JXpVruR11MomKhPraDkrFpXkrbXdZcRBQb+egjKPxwwzxiVfcGJbJ1fbWrBZdXI0JV/Fmd+p3PMbJktZ6inf+vBMAMU0xAuh8lwL24chUL3id/Tii0ADqbzxdw5lCKoD7HG3hhb5bCxTtZUwhQoLfgOhgIKH5AdQh6Cwpt1TsF0hsA/35xKw7JXTBUijvGh9X6NNdrI6r9Fup+J532eCZQIwxm+/jIKfSKou1iHgbRl5RlMbaBZpI2Hir1qcLBZyrc7E2Q0i13mYw== enki@openclaw
EOF

chmod 600 ~/.ssh/authorized_keys
echo "✅ Enki's SSH key added!"
