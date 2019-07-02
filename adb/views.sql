CREATE VIEW mapping_view AS
    SELECT m.id,

       sc.namespace as source_namespace,
       sc.miriam as source_miriam,
       source.term as source_term,
       m.qualifier,
       tc.namespace as target_namespace,
       tc.miriam as target_miriam,
       target.term as target_term,
       evidence.source as evidence_source,
       evidence.version as evidence_version,
       evidence.evidence as evidence

       FROM adb_mapping m
            INNER JOIN adb_annotation source ON (m.source_id = source.id)
            INNER JOIN adb_annotation target ON (m.target_id = target.id)
            INNER JOIN adb_evidence evidence ON (m.evidence_id = evidence.id)
            INNER JOIN adb_collection sc ON (source.collection_id = sc.id)
            INNER JOIN adb_collection tc ON (target.collection_id = tc.id);
