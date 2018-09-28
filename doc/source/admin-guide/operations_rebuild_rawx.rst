======================
Rebuild a Volume: Rawx
======================

.. contents::
   :local:

Preparation
~~~~~~~~~~~

Find information about the service you want to rebuild.
By running ``openio cluster list rawx`` you will get a list of all rawx service IDs accompanied by their volume paths.

Verify that the service was automatically scored to zero by running ``openio cluster list rawx``.

If not, lock the score of the targeted rawx service to zero by running ``openio cluster lock rawx <RAWX_ID>``, where RAWX_ID is the network address of the service (ip:port).
This will prevent the service from receiving upload requests, and will reduce the number of download requests.

Set the incident date
~~~~~~~~~~~~~~~~~~~~~

Set an incident on the target rawx service by running the ``openio volume admin`` command:

  .. code-block:: console

     # openio volume admin incident <RAWX_ID>

     +----------------+------------+
     | Volume         |       Date |
     +----------------+------------+
     | 127.0.0.1:6025 | 1537262799 |
     +----------------+------------+

By default, the incident date is the current timestamp. You can change this incident date by using the parameter ``--date <TIMESTAMP>``.

Check that the incident date is correctly set:

  .. code-block:: console

     # openio volume admin show <RAWX_ID>

     +---------------+----------------+
     | Field         | Value          |
     +---------------+----------------+
     | volume        | 127.0.0.1:6025 |
     | incident_date | 1537262799     |
     +---------------+----------------+

Launch rebuilding
~~~~~~~~~~~~~~~~~

You can now launch the rebuild by using the ``oio-blob-rebuilder`` tool:

  .. code-block:: console

    # oio-blob-rebuilder <NAMESPACE> --volume <RAWX_ID>

    25661 7FCEB9EC7EB0 log INFO START volume=127.0.0.1:6025 last_report=2018-09-27T12:17:46 0.00s chunks=0 0.00/s bytes=0 0.00B/s errors=0 0.00% start_time=2018-09-27T12:17:46 0.00s total_chunks=0 0.00/s total_bytes=0 0.00B/s total_errors=0 0.00% progress=0/1490 0.00%
    25661 7FCEB90F22D0 log INFO RUN volume=127.0.0.1:6025 last_report=2018-09-27T12:17:46 10.09s chunks=275 27.25/s bytes=184766464 18307632.15B/s errors=0 0.00% start_time=2018-09-27T12:17:46 10.09s total_chunks=275 27.25/s total_bytes=184766464 18307628.26B/s total_errors=0 0.00% progress=275/1490 18.46%
    [...]
    25661 7FCEB90F20F0 log INFO RUN volume=127.0.0.1:6025 last_report=2018-09-27T12:18:27 10.29s chunks=271 26.34/s bytes=189318144 18402483.44B/s errors=0 0.00% start_time=2018-09-27T12:17:46 51.25s total_chunks=1374 26.81/s total_bytes=956872704 18671525.55B/s total_errors=0 0.00% progress=1374/1490 92.21%
    25661 7FCEB9EC7EB0 log INFO DONE volume=127.0.0.1:6025 last_report=2018-09-27T12:18:38 4.11s chunks=116 28.20/s bytes=79408128 19306981.87B/s errors=0 0.00% start_time=2018-09-27T12:17:46 55.36s total_chunks=1490 26.91/s total_bytes=1036280832 18718735.70B/s total_errors=0 0.00% progress=1490/1490 100.00%

Clear the incident date
~~~~~~~~~~~~~~~~~~~~~~~

After the rebuilding and if there were no errors, you can clear the incident.

.. code-block:: console

   # openio volume admin clear --before-incident <RAWX_ID>

   +----------------+---------+--------------------------------------------+
   | Volume         | Success | Message                                    |
   +----------------+---------+--------------------------------------------+
   | 127.0.0.1:6025 | True    | {'removed': 0, 'repaired': 0, 'errors': 0} |
   +----------------+---------+--------------------------------------------+

   # openio volume admin show <RAWX_ID>

   +--------+----------------+
   | Field  | Value          |
   +--------+----------------+
   | volume | 127.0.0.1:6025 |
   +--------+----------------+

Distribute rebuilding
~~~~~~~~~~~~~~~~~~~~~

To distribute, we use the Master/Slave model. The broken chunks are sent to beanstalkd tubes and the slave rebuilders listen to these beanstalkd tubes.

You can start a slave:

.. code-block:: console

   # oio-blob-rebuilder <NAMESPACE> --beanstalkd <SLAVE1_IP:SLAVE1_PORT>


You can start the master:

.. code-block:: console

   # oio-blob-rebuilder <NAMESPACE> --volume <RAWX_ID> --distributed <SLAVE1_IP:SLAVE1_PORT;SLAVE2_IP:SLAVE2_PORT;...> --beanstalkd <MASTER_IP:MASTER_PORT> --beanstalkd-tube oio-rebuilt

The slaves must be started before the master.
