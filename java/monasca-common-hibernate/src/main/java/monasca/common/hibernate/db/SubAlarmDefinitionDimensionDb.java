/*
 * Copyright (c) 2014 Hewlett-Packard Development Company, L.P.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
 * implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package monasca.common.hibernate.db;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

@Entity
@Table(name = "sub_alarm_definition_dimension")
public class SubAlarmDefinitionDimensionDb implements Serializable {

  @EmbeddedId
  SubAlarmDefinitionDimensionId subAlarmDefinitionDimensionId;

  @Column(name = "value", length = 36, nullable = true)
  private String value;

  public SubAlarmDefinitionDimensionDb() {
    this("", "", null);
  }

  public SubAlarmDefinitionDimensionDb(SubAlarmDefinitionDimensionId subAlarmDefinitionDimensionId) {
    super();
    this.subAlarmDefinitionDimensionId = subAlarmDefinitionDimensionId;
  }

  public SubAlarmDefinitionDimensionDb(String sub_alarm_definition_id, String dimension_name, String value) {
    super();
    this.subAlarmDefinitionDimensionId = new SubAlarmDefinitionDimensionId(sub_alarm_definition_id, dimension_name);
    this.value = value;
  }

  public SubAlarmDefinitionDimensionDb(SubAlarmDefinitionDimensionId subAlarmDefinitionDimensionId, String value) {
    super();
    this.subAlarmDefinitionDimensionId = subAlarmDefinitionDimensionId;
    this.value = value;
  }

  public SubAlarmDefinitionDimensionId getSubAlarmDefinitionDimensionId() {
    return subAlarmDefinitionDimensionId;
  }

  public void setSubAlarmDefinitionDimensionId(SubAlarmDefinitionDimensionId subAlarmDefinitionDimensionId) {
    this.subAlarmDefinitionDimensionId = subAlarmDefinitionDimensionId;
  }

  public String getValue() {
    return value;
  }

  public void setValue(String value) {
    this.value = value;
  }
}
