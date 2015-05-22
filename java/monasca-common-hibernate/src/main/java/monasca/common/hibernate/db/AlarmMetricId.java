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

import java.io.Serializable;
import java.util.UUID;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.Lob;

import org.hibernate.annotations.Type;

@Embeddable
public class AlarmMetricId implements Serializable {

  @Column(name = "alarm_id", length = 36)
  protected String alarm_id;

  @Column(name = "metric_definition_dimensions_id", length = 20, updatable = false, nullable = false)
  @Lob
  @Type(type = "org.hibernate.type.UUIDBinaryType")
  protected UUID metric_definition_dimensions_id;

  public AlarmMetricId() {
    this("", DbUtils.toUUID(DbUtils.DEFAULT_VALUE));
  }

  public AlarmMetricId(String alarm_id, byte[] metric_definition_dimensions_id) {
    this(alarm_id, DbUtils.toUUID(metric_definition_dimensions_id));
  }

  public AlarmMetricId(String alarm_id, UUID metric_definition_dimensions_id) {
    super();
    this.alarm_id = alarm_id;
    this.metric_definition_dimensions_id = metric_definition_dimensions_id;
  }

  public AlarmMetricId(String alarm_id) {
    this(alarm_id, DbUtils.toUUID(DbUtils.DEFAULT_VALUE));
  }

  public String getAlarm_id() {
    return alarm_id;
  }

  public void setAlarm_id(String alarm_id) {
    this.alarm_id = alarm_id;
  }

  public byte[] getMetric_definition_dimensions_id() {
    return DbUtils.toByteArray(metric_definition_dimensions_id);
  }

  public void setMetric_definition_dimensions_id(byte[] metric_definition_dimensions_id) {
    this.metric_definition_dimensions_id = DbUtils.toUUID(metric_definition_dimensions_id);
  }

  public void setMetric_definition_dimensions_id(UUID metric_definition_dimensions_id) {
    this.metric_definition_dimensions_id = metric_definition_dimensions_id;
  }

  @Override
  public int hashCode() {
    final int prime = 31;
    int result = 1;
    result = prime * result + ((alarm_id == null) ? 0 : alarm_id.hashCode());
    result = prime * result + ((metric_definition_dimensions_id == null) ? 0 : metric_definition_dimensions_id.hashCode());
    return result;
  }

  @Override
  public boolean equals(Object obj) {
    if (this == obj)
      return true;
    if (obj == null)
      return false;
    if (getClass() != obj.getClass())
      return false;
    AlarmMetricId other = (AlarmMetricId) obj;
    if (alarm_id == null) {
      if (other.alarm_id != null)
        return false;
    } else if (!alarm_id.equals(other.alarm_id))
      return false;
    if (metric_definition_dimensions_id == null) {
      if (other.metric_definition_dimensions_id != null)
        return false;
    } else if (!metric_definition_dimensions_id.equals(other.metric_definition_dimensions_id))
      return false;
    return true;
  }
}
