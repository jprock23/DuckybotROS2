from setuptools import find_packages, setup

package_name = 'motor_driver'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jproque',
    maintainer_email='juanproque@outlook.com',
    description='Package for a motor driver that controls a motor on the duckiebot DB-19.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motor=motor_driver.motor_node:main',
        ],
    },
)
