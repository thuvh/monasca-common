/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.hibernate.db;

import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;

import org.hibernate.annotations.Type;


@Entity
@Table(name = "metric_definition_dimensions")
public class MetricDefinitionDimensionsDb {

  @Id
  @Column(name = "id", length = 20)
  @Lob
  @Type(type = "org.hibernate.type.UUIDBinaryType")
  private UUID id;

  @Column(name = "metric_definition_id", length = 20, nullable = false)
  @Lob
  @Type(type = "org.hibernate.type.UUIDBinaryType")
  private UUID metric_definition_id;

  @Column(name = "metric_dimension_set_id", length = 20, nullable = false)
  @Lob
  @Type(type = "org.hibernate.type.UUIDBinaryType")
  private UUID metric_dimension_set_id;

  public MetricDefinitionDimensionsDb() {
    this(DbUtils.toUUID(DbUtils.DEFAULT_VALUE), DbUtils.toUUID(DbUtils.DEFAULT_VALUE), DbUtils.toUUID(DbUtils.DEFAULT_VALUE));

  }

  public MetricDefinitionDimensionsDb(UUID id, UUID metric_definition_id, UUID metric_dimension_set_id) {
    super();
    this.id = id;
    this.metric_definition_id = metric_definition_id;
    this.metric_dimension_set_id = metric_dimension_set_id;
  }

  public MetricDefinitionDimensionsDb(byte[] id, byte[] metric_definition_id, byte[] metric_dimension_set_id) {
    this(DbUtils.toUUID(id), DbUtils.toUUID(metric_definition_id), DbUtils.toUUID(metric_dimension_set_id));
  }

  public UUID getId() {
    return id;
  }

  public void setId(UUID id) {
    this.id = id;
  }

  public UUID getMetric_definition_id() {
    return metric_definition_id;
  }

  public void setMetric_definition_id(UUID metric_definition_id) {
    this.metric_definition_id = metric_definition_id;
  }

  public UUID getMetric_dimension_set_id() {
    return metric_dimension_set_id;
  }

  public void setMetric_dimension_set_id(UUID metric_dimension_set_id) {
    this.metric_dimension_set_id = metric_dimension_set_id;
  }
}
