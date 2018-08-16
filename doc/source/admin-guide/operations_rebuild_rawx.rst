======================
Rebuild a Volume: Rawx
======================

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

By default, the incident date is the current timestamp. You can change this incident date by using the parameter ``--date <TIMESTAMP>``.

Check that the incident date is correctly set:

  .. code-block:: console

     # openio volume admin show <RAWX_ID>

     +---------------+-----------------+
     | Field         | Value           |
     +---------------+-----------------+
     | volume        | 10.0.0.186:6004 |`
     | incident_date | 1484517814      |
     +---------------+-----------------+

Launch rebuilding
~~~~~~~~~~~~~~~~~

You can now launch the rebuild by using the ``oio-blob-rebuilder`` tool:

  .. code-block:: console

    # oio-blob-rebuilder <NAMESPACE> --volume <RAWX_ID>
